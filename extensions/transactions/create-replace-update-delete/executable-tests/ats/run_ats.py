#!/usr/bin/env python3
"""
Executable test runner for the Abstract Test Suite (Annex A) of the draft
OGC API - Features - Part 4 / OGC API - Common - Part 5:
Create, Replace, Update and Delete (OGC 20-002).

Implements the 34 abstract tests. Each test evaluates its "Condition" row
against the conformance declaration of the Web API under test and the
Mutable Resources test parameter; tests whose condition is not met are
reported as SKIP. Only the Python 3 standard library is required.

The tests use the test dataset of this Standard (../standard/data): a feature
collection with the features B.1, B.2, B.3 and the request bodies
create-building.json, create-building-invalid.json, create-building-jsonfg.json,
create-building.gml, replace-building.json, replace-building.gml and
update-building.json.

The Web API under test is identified by its landing page URI (--landing-page)
and the collection that publishes the test dataset (--collection); see
run-tests.sh for the deployment used to validate the test suite.

Since the tests mutate resources, the dataset must be reset between
conformance classes; pass a shell command that reloads the dataset via
--reset-cmd (e.g. a psql call in the database container).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import email.utils
from datetime import datetime, timedelta, timezone
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlsplit, urljoin, quote

GEOJSON = "application/geo+json"
MERGE_PATCH = "application/merge-patch+json"
GML = "application/gml+xml"
SCHEMA_JSON = "application/schema+json"
ACCEPT_FEATURE = "application/geo+json,application/json;q=0.8"
PROFILE_RFC7946 = "http://www.opengis.net/def/profile/OGC/0/rfc7946"
PROFILE_JSONFG = "http://www.opengis.net/def/profile/OGC/0/jsonfg"
CRS84 = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"

# The conformance class URIs of this Standard and of the Standards that its
# conformance classes depend on. The five conformance classes that are shared
# with OGC API - Common - Part 5 use the "ogcapi-common-5" URIs of the
# conformance declaration table in clause 2, the Features conformance class is
# specific to OGC API - Features - Part 4.
CONF = {
    "create-replace-delete":
        "http://www.opengis.net/spec/ogcapi-common-5/1.0/conf/create-replace-delete",
    "update":
        "http://www.opengis.net/spec/ogcapi-common-5/1.0/conf/update",
    "optimistic-locking-timestamps":
        "http://www.opengis.net/spec/ogcapi-common-5/1.0/conf/optimistic-locking-timestamps",
    "optimistic-locking-etags":
        "http://www.opengis.net/spec/ogcapi-common-5/1.0/conf/optimistic-locking-etags",
    "handling":
        "http://www.opengis.net/spec/ogcapi-common-5/1.0/conf/handling",
    "features":
        "http://www.opengis.net/spec/ogcapi-features-4/1.0/conf/features",
    "oaf-core":
        "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
    "geojson":
        "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
    "gmlsf0":
        "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/gmlsf0",
    "gmlsf2":
        "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/gmlsf2",
    "crs":
        "http://www.opengis.net/spec/ogcapi-features-2/1.0/conf/crs",
    "schemas":
        "http://www.opengis.net/spec/ogcapi-common-3/1.0/conf/returnables-and-receivables",
    "jsonfg-api":
        "http://www.opengis.net/spec/json-fg-1/1.0/conf/api",
}

STEP = None      # description of what the next request tests (verbose output)
CFG = None       # argparse namespace
DATA = {}        # loaded test dataset files
CONFORMS = []    # declared conformance URIs
STATE = {}       # cross-test state (e.g. whether PUT-create is supported)
NOTES = []       # informational findings


# ---------------------------------------------------------------- HTTP layer

class Response:
    def __init__(self, status, reason, headers, body, url):
        self.status = status
        self.reason = reason
        self.headers = headers  # list of (name, value)
        self.body = body
        self.url = url

    def header(self, name):
        vals = [v for k, v in self.headers if k.lower() == name.lower()]
        return ", ".join(vals) if vals else None

    def json(self):
        try:
            return json.loads(self.body)
        except Exception as e:
            raise Fail(f"response from {self.url} is not valid JSON ({e}); "
                       f"body starts with: {self.body[:200]!r}")

    def summary(self):
        body = re.sub(r"\s+", " ", self.body[:500].decode("utf-8", "replace")).strip()
        return f"[{self.status} {self.reason}] {body[:250]}"


def rq(method, url, body=None, ctype=None, headers=None, accept=None):
    """HTTP request without any implicit headers (so that e.g. a missing
    Content-Type header is really missing)."""
    parts = urlsplit(url)
    conn_cls = HTTPSConnection if parts.scheme == "https" else HTTPConnection
    conn = conn_cls(parts.hostname, parts.port, timeout=CFG.timeout)
    path = parts.path or "/"
    if parts.query:
        path += "?" + parts.query
    hdrs = {}
    if accept is None and method in ("POST", "PUT", "PATCH", "DELETE"):
        accept = "application/json,application/geo+json;q=0.9"
    if accept:
        hdrs["Accept"] = accept
    if ctype:
        hdrs["Content-Type"] = ctype
    if headers:
        hdrs.update(headers)
    if isinstance(body, (dict, list)):
        body = json.dumps(body).encode("utf-8")
    try:
        conn.request(method, path, body=body, headers=hdrs)
        r = conn.getresponse()
        resp = Response(r.status, r.reason, r.getheaders(), r.read(), url)
    finally:
        conn.close()
    if CFG.verbose:
        global STEP
        if STEP:
            print(f"      · {STEP}")
            STEP = None
        print(f"      > {method} {url} -> {resp.status}")
    return resp


# ------------------------------------------------------------ test framework

class Skip(Exception):
    pass


class Fail(Exception):
    pass


TESTS = []


def ats(cls, name, purpose=""):
    def deco(fn):
        TESTS.append((cls, name, fn, purpose))
        return fn
    return deco


def step(msg):
    """Describe what the next request tests (shown with --verbose)."""
    global STEP
    STEP = msg


def step_more(msg):
    """Add a qualification to the description of the next request."""
    global STEP
    STEP = f"{STEP} — {msg}" if STEP else msg


def step_default(msg):
    """Describe the next request, unless the test already described it."""
    global STEP
    if STEP is None:
        STEP = msg


def check(cond, msg, resp=None):
    if not cond:
        raise Fail(msg + (f" — {resp.summary()}" if resp is not None else ""))


def note(msg):
    NOTES.append(msg)
    print(f"      NOTE: {msg}")


def declares(key):
    if key in CFG.assume:
        return True
    return CONF[key] in CONFORMS


# ------------------------------------------------------------------- helpers

def items_url(coll=None):
    return f"{CFG.landing_page}/collections/{coll or CFG.collection}/items"


def feat_url(fid, coll=None):
    return items_url(coll) + "/" + quote(str(fid), safe="")


def list_ids(coll=None):
    step_default("list the features of the collection")
    r = rq("GET", items_url(coll) + "?limit=1000", accept=ACCEPT_FEATURE)
    check(r.status == 200, f"GET {items_url(coll)} failed", r)
    return [f.get("id") for f in r.json().get("features", [])]


def get_feature(fid_or_url, coll=None):
    url = fid_or_url if fid_or_url.startswith("http") else feat_url(fid_or_url, coll)
    step_default("retrieve the feature to evaluate the assertions about its state")
    return rq("GET", url, accept=ACCEPT_FEATURE)


def num_eq(a, b, tol):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(num_eq(x, y, tol) for x, y in zip(a, b))
    return a == b


def geom_eq(g1, g2, tol=1e-6):
    if g1 is None or g2 is None:
        return g1 is None and g2 is None
    return g1.get("type") == g2.get("type") and num_eq(
        g1.get("coordinates"), g2.get("coordinates"), tol)


def props_match(expected, actual, tol=1e-6):
    """Each submitted property must be present with the submitted value;
    server-managed extras (e.g. 'updated') are ignored."""
    actual = actual or {}
    for k, v in (expected or {}).items():
        if v is None:
            if actual.get(k) is not None:
                return f"property '{k}' should be unset/null, is {actual.get(k)!r}"
        elif not num_eq(v, actual.get(k), tol):
            return f"property '{k}': expected {v!r}, got {actual.get(k)!r}"
    return None


def feature_matches(submitted, actual, tol=1e-6, ignore_geometry=False):
    err = props_match(submitted.get("properties"), actual.get("properties"), tol)
    if err:
        raise Fail(f"feature does not match the submitted representation: {err}")
    if not ignore_geometry and submitted.get("geometry") is not None:
        if not geom_eq(submitted["geometry"], actual.get("geometry"), tol):
            raise Fail("feature geometry does not match the submitted geometry: "
                       f"{json.dumps(actual.get('geometry'))[:200]}")


def location_of(resp):
    loc = resp.header("Location")
    check(loc is not None, "response does not include a Location header", resp)
    return urljoin(resp.url + "/", loc)


def parse_http_date(value):
    try:
        return email.utils.parsedate_to_datetime(value)
    except Exception:
        raise Fail(f"'{value}' is not a valid HTTP-date")


def http_date(dt):
    return email.utils.format_datetime(dt, usegmt=True)


def queued(resp):
    """A 202 means the operation was queued; per Annex A the remaining
    assertions are skipped (a poll-until-visible strategy is permitted,
    ldproxy responds synchronously so this branch is not exercised)."""
    if resp.status == 202:
        note(f"{resp.url}: 202 (queued) — remaining assertions skipped")
        return True
    return False


def last_modified_or_now(fid=None):
    if fid:
        step("determine the current Last-Modified value of the feature for the "
             "precondition of the next request")
        g = get_feature(fid)
        lm = g.header("Last-Modified")
        if g.status == 200 and lm:
            return lm
    return http_date(datetime.now(timezone.utc))


_noted = set()


def note_once(key, msg):
    if key not in _noted:
        _noted.add(key)
        note(msg)


def precond_headers(fid=None):
    """If the API declares Optimistic Locking using Timestamps, it may require
    a precondition on every mutation request (permitted by the OL class)."""
    if declares("optimistic-locking-timestamps"):
        return {"If-Unmodified-Since": last_modified_or_now(fid)}
    return {}


def mutate(method, url, body=None, ctype=None, headers=None, fid=None):
    """Mutation request; if the unconditional request is rejected and the API
    declares Optimistic Locking using Timestamps, retry with a precondition
    and record the discrepancy (the Create/Replace/Delete and Update tests
    assume unconditional requests succeed)."""
    if (declares("optimistic-locking-timestamps")
            and "If-Unmodified-Since" not in (headers or {})):
        step_more("sent without a precondition first; a server that requires one "
                  "rejects it (428 or 409, some servers 400) and the request is "
                  "then repeated with the precondition")
    r = rq(method, url, body, ctype, headers=headers)
    if (r.status in (400, 409, 428)
            and declares("optimistic-locking-timestamps")
            and "If-Unmodified-Since" not in (headers or {})):
        h = dict(headers or {})
        h["If-Unmodified-Since"] = last_modified_or_now(fid)
        step(f"repeat the {method} request with an If-Unmodified-Since header, "
             "because the server requires a precondition")
        r2 = rq(method, url, body, ctype, headers=h)
        if fid:
            note_once("unconditional-mutation",
                      f"the server rejected an unconditional {method} with {r.status} "
                      "and the request was repeated with an If-Unmodified-Since "
                      "header, as described in the introduction of Annex A "
                      "(permitted by /per/optimistic-locking-timestamps/"
                      "ifunmodifiedsince-missing)")
        else:
            note_once("unconditional-create",
                      f"the server rejected a {method} to a non-existing resource "
                      f"with {r.status}, i.e. it requires a precondition although "
                      "the resource does not exist yet; the request was repeated "
                      "with the current time as the precondition. The requirements "
                      "of the Optimistic Locking classes only cover an operation "
                      "that replaces or updates an existing resource")
        return r2
    return r


def media_types(resp, header):
    """The media types of an Accept-Post / Accept-Patch header."""
    v = resp.header(header)
    return [m.strip().split(";")[0].strip().lower() for m in v.split(",")] if v else []


def supports_media_type(mt, operation, coll=None):
    """Does the server support a media type in the request body of an operation?
    Determined from the Accept-Post (CREATE) or Accept-Patch (UPDATE) header of
    the OPTIONS response. If the header is absent, support cannot be determined
    from it and the test proceeds, treating a 415 response as "not supported"
    (see the introduction of Annex A); the missing header is reported by the
    tests of the OPTIONS operation."""
    mt = mt.split(";")[0].strip().lower()
    header = {"CREATE": "Accept-Post", "UPDATE": "Accept-Patch"}[operation]
    url = items_url(coll) if operation == "CREATE" else feat_url(list_ids(coll)[0], coll)
    step(f"determine from the {header} header of the OPTIONS response whether the "
         f"server supports {mt} in {operation} requests (condition of the test)")
    advertised = media_types(rq("OPTIONS", url), header)
    if not advertised:
        note_once(f"no-{header}",
                  f"the OPTIONS response has no {header} header, so the supported "
                  "media types cannot be determined from it; a 415 response is "
                  "used instead")
        return True
    return mt in advertised


def allow_methods(resp):
    allow = resp.header("Allow")
    check(allow is not None, "response does not include an Allow header", resp)
    return [m.strip().upper() for m in allow.split(",")]


def collection_doc(coll=None):
    url = f"{CFG.landing_page}/collections/{coll or CFG.collection}"
    step_default("retrieve the collection resource")
    r = rq("GET", url, accept="application/json")
    check(r.status == 200, f"GET {url} failed", r)
    return r.json()


def collection_crs_list(coll):
    crs = list(coll.get("crs", []))
    if "#/crs" in crs:
        crs.remove("#/crs")
        step_default("retrieve the collections resource for the shared list of "
                     "coordinate reference systems")
        r = rq("GET", f"{CFG.landing_page}/collections", accept="application/json")
        crs += r.json().get("crs", [])
    return crs


# =====================================================================
# Conformance Class "Create/Replace/Delete"
# =====================================================================

@ats("create-replace-delete", "options",
     "The server declares the supported methods for each mutable resource")
def test_crd_options():
    step("OPTIONS on the resources endpoint: the server declares the supported "
         "methods and the media types accepted for CREATE")
    r = rq("OPTIONS", items_url())
    check(r.status == 200, "OPTIONS on the resources endpoint must return 200", r)
    methods = allow_methods(r)
    check("POST" in methods, f"Allow header of the resources endpoint must list POST, got {methods}")
    check(media_types(r, "Accept-Post"),
          "a response whose Allow header includes POST must include an Accept-Post "
          "header with at least one media type", r)
    for fid in list_ids():
        step("OPTIONS on the resource endpoint: the server declares the methods "
             "for REPLACE, UPDATE and DELETE")
        r = rq("OPTIONS", feat_url(fid))
        check(r.status == 200, f"OPTIONS on {feat_url(fid)} must return 200", r)
        methods = allow_methods(r)
        for m in ("PUT", "DELETE") + (("PATCH",) if declares("update") else ()):
            check(m in methods, f"Allow header of {feat_url(fid)} must list {m}, got {methods}")


@ats("create-replace-delete", "create",
     "Adding a new resource to a collection")
def test_crd_create():
    ids_before = list_ids()
    body = DATA["create-building.json"]
    step("POST a valid new feature: the resource is created (201) and the response "
         "has a Location header")
    r = rq("POST", items_url(), body, GEOJSON)
    if queued(r):
        return
    check(r.status == 201, "POST with a new resource must return 201", r)
    loc = location_of(r)
    step("GET the URI from the Location header: it returns the submitted feature "
         "with a new identifier")
    g = rq("GET", loc, accept=ACCEPT_FEATURE)
    check(g.status == 200, f"GET {loc} must return 200", g)
    new = g.json()
    feature_matches(body, new)
    check(new.get("id") not in ids_before,
          f"the identifier of the new resource ({new.get('id')!r}) must differ from existing identifiers")


@ats("create-replace-delete", "create-content-type",
     "CREATE requests without a Content-Type header are rejected")
def test_crd_create_content_type():
    body = json.dumps(DATA["create-building.json"]).encode()
    step("POST without a Content-Type header: the request is rejected with 400")
    r = rq("POST", items_url(), body, ctype=None)
    check(r.status == 400, "POST without a Content-Type header must be rejected with 400", r)


@ats("create-replace-delete", "replace",
     "Replacing the content of an existing resource")
def test_crd_replace():
    body = DATA["replace-building.json"]
    step("PUT new content for an existing feature: the content is replaced "
         "(200 or 204)")
    r = mutate("PUT", feat_url("B.2"), body, GEOJSON, fid="B.2")
    if queued(r):
        return
    check(r.status in (200, 204), "PUT replacing an existing resource must return 200 or 204", r)
    g = get_feature("B.2")
    check(g.status == 200, "GET after REPLACE must return 200", g)
    feature_matches(body, g.json())


@ats("create-replace-delete", "replace-content-type",
     "REPLACE requests without a Content-Type header are rejected")
def test_crd_replace_content_type():
    body = json.dumps(DATA["replace-building.json"]).encode()
    step("PUT without a Content-Type header: the request is rejected with 400")
    r = rq("PUT", feat_url("B.1"), body, ctype=None, headers=precond_headers("B.1"))
    check(r.status == 400, "PUT without a Content-Type header must be rejected with 400", r)


@ats("create-replace-delete", "replace-rid",
     "Resource identifiers in REPLACE request bodies are ignored or the request is rejected")
def test_crd_replace_rid():
    body = dict(DATA["replace-building.json"])
    body["id"] = "B.999"
    step("PUT content with a different resource identifier in the body: the "
         "identifier is ignored (or the request is rejected)")
    r = mutate("PUT", feat_url("B.1"), body, GEOJSON, fid="B.1")
    if queued(r):
        return
    if 400 <= r.status < 500:
        note(f"replace-rid: the request was rejected with {r.status}; for features "
             "either behaviour is permitted, /req/features/geojson-create-replace A "
             "allows ignoring the 'id' member or rejecting the request")
        return
    check(r.status in (200, 204), "PUT must return 200 or 204 (or a 4xx rejection)", r)
    g = get_feature("B.1")
    check(g.status == 200, "GET after REPLACE must return 200", g)
    check(g.json().get("id") == "B.1",
          f"the resource must keep the identifier from the URI, got {g.json().get('id')!r}")
    step("GET the identifier that was submitted in the body: no resource was "
         "created under it")
    g999 = get_feature("B.999")
    check(g999.status == 404,
          "no resource with the identifier from the request body may have been created", g999)


@ats("create-replace-delete", "replace-exceptions",
     "PUT requests to non-existing resources are handled correctly")
def test_crd_replace_exceptions():
    """Executed for every mutable feature collection: the collection with
    auto-generated ids exercises the 404 branch, the collection with
    client-assigned ids (test parameter --put-create-collection) the branch
    where PUT creates the resource (upsert)."""
    body = DATA["create-building.json"]
    colls = [None] + ([CFG.put_create_collection] if CFG.put_create_collection else [])
    for coll in colls:
        label = coll or CFG.collection
        step(f"[{label}] PUT to a non-existing resource: either 404, or the "
             "resource is created (201)")
        r1 = mutate("PUT", feat_url("B.900", coll), body, GEOJSON)
        if r1.status == 404:
            STATE.setdefault("put-create", False)
            STATE["put-create-" + label] = False
            note(f"replace-exceptions [{label}]: PUT to a non-existing resource "
                 "returns 404 (creating resources with PUT is not supported)")
        elif r1.status in (201, 202):
            STATE["put-create"] = True
            STATE["put-create-" + label] = True
            note(f"replace-exceptions [{label}]: PUT to a non-existing resource "
                 f"returns {r1.status} (upsert)")
            if r1.status != 202:
                g = get_feature("B.900", coll)
                check(g.status == 200, f"[{label}] GET after a successful PUT-create "
                                       "must return 200", g)
                feature_matches(body, g.json())
        else:
            raise Fail(f"[{label}] PUT to a non-existing resource must return 404 "
                       f"(creating resources with PUT not supported) or 201 — or 202, "
                       f"if the operation has been queued — {r1.summary()}")
        upsert = STATE.get("put-create-" + label, False)
        step(f"[{label}] PUT to a non-existing resource with an If-Match header: "
             + ("the precondition fails (412) and nothing is created" if upsert else
                "the request is unsuccessful independently of the precondition, so "
                "the response is 404 (RFC 9110, section 13.2.1)"))
        r2 = rq("PUT", feat_url("B.901", coll), body, GEOJSON,
                headers={"If-Match": '"xyz"'})
        if upsert:
            check(r2.status == 412,
                  f"[{label}] PUT with a non-matching If-Match header must return 412, "
                  "because the server supports creating resources with PUT", r2)
        else:
            check(r2.status == 404,
                  f"[{label}] PUT with a non-matching If-Match header must return 404, "
                  "because the request is unsuccessful independently of the "
                  "precondition (RFC 9110, section 13.2.1)", r2)
        g = get_feature("B.901", coll)
        check(g.status == 404,
              f"[{label}] no resource may have been created by the rejected "
              "conditional PUT", g)


@ats("create-replace-delete", "delete",
     "Removing an existing resource from a collection")
def test_crd_delete():
    step("DELETE an existing feature: it is removed (200 or 204)")
    r = mutate("DELETE", feat_url("B.3"), fid="B.3")
    if queued(r):
        return
    check(r.status in (200, 204), "DELETE must return 200 or 204", r)
    g = get_feature("B.3")
    check(g.status == 404, "GET after DELETE must return 404", g)


# =====================================================================
# Conformance Class "Update"
# =====================================================================

@ats("update", "options",
     "The server declares support for the PATCH method")
def test_upd_options():
    for fid in list_ids():
        step("OPTIONS on the resource endpoint: the server declares PATCH and the "
             "media types accepted for UPDATE")
        r = rq("OPTIONS", feat_url(fid))
        check(r.status == 200, f"OPTIONS on {feat_url(fid)} must return 200", r)
        check("PATCH" in allow_methods(r),
              f"Allow header of {feat_url(fid)} must include PATCH")
        check(media_types(r, "Accept-Patch"),
              f"the OPTIONS response for {feat_url(fid)} must include an Accept-Patch "
              "header with at least one media type", r)


@ats("update", "update",
     "Updating parts of an existing resource")
def test_upd_update():
    pre = get_feature("B.3")
    check(pre.status == 200, "GET before UPDATE must return 200", pre)
    pre = pre.json()
    patch = DATA["update-building.json"]
    step("PATCH with a document describing the changes: the described parts are "
         "changed, everything else is unchanged")
    r = mutate("PATCH", feat_url("B.3"), patch, MERGE_PATCH, fid="B.3")
    if queued(r):
        return
    check(r.status in (200, 204), "PATCH must return 200 or 204", r)
    g = get_feature("B.3")
    check(g.status == 200, "GET after UPDATE must return 200", g)
    f = g.json()
    err = props_match(patch.get("properties"), f.get("properties"))
    check(err is None, f"the changes have not been applied: {err}")
    check(geom_eq(patch["geometry"], f.get("geometry")),
          f"the geometry has not been changed: {json.dumps(f.get('geometry'))[:200]}")
    # all other parts unchanged
    check(f.get("id") == "B.3", "the identifier must be unchanged")
    for k, v in pre.get("properties", {}).items():
        if k in patch.get("properties", {}) or k == "updated":
            continue
        check(num_eq(f.get("properties", {}).get(k), v, 1e-6),
              f"the property '{k}' must be unchanged: expected {v!r}, got {f.get('properties', {}).get(k)!r}")


@ats("update", "update-content-type",
     "UPDATE requests without a Content-Type header are rejected")
def test_upd_content_type():
    body = json.dumps(DATA["update-building.json"]).encode()
    step("PATCH without a Content-Type header: the request is rejected with 400")
    r = rq("PATCH", feat_url("B.3"), body, ctype=None, headers=precond_headers("B.3"))
    check(r.status == 400, "PATCH without a Content-Type header must be rejected with 400", r)


@ats("update", "update-rid",
     "Resource identifiers in UPDATE request bodies are ignored or the request is rejected")
def test_upd_update_rid():
    step("PATCH a document with a different resource identifier: the identifier "
         "is ignored (or the request is rejected)")
    r = mutate("PATCH", feat_url("B.3"), {"id": "B.999"}, MERGE_PATCH, fid="B.3")
    if queued(r):
        return
    if 400 <= r.status < 500:
        note(f"update-rid: the request was rejected with {r.status}, which for "
             "features is required: /req/features/update-json-merge-patch B requires "
             "that a document which changes the property with the role 'id' is "
             "rejected (the requirement does not prescribe the status code)")
        return
    check(r.status in (200, 204), "PATCH must return 200 or 204 (or a 4xx rejection)", r)
    g = get_feature("B.3")
    check(g.status == 200, "GET after UPDATE must return 200", g)
    check(g.json().get("id") == "B.3",
          f"the resource must keep the identifier from the URI, got {g.json().get('id')!r}")


# =====================================================================
# Conformance Class "Optimistic Locking using Timestamps"
# =====================================================================

@ats("optimistic-locking-timestamps", "get-last-modified",
     "Resource representations include a Last-Modified header")
def test_olt_get():
    for fid in list_ids():
        step("GET the feature: the response has a Last-Modified header with a "
             "valid HTTP-date")
        r = get_feature(fid)
        check(r.status == 200, f"GET {feat_url(fid)} must return 200", r)
        lm = r.header("Last-Modified")
        check(lm is not None, f"the response for {fid} must include a Last-Modified header", r)
        parse_http_date(lm)


def _olt_conditional(method, fid, body, ctype):
    step("GET the feature to obtain its Last-Modified value for the preconditions")
    g = get_feature(fid)
    check(g.status == 200, "GET before the conditional requests must return 200", g)
    name_before = g.json().get("properties", {}).get("name")
    lm = g.header("Last-Modified")
    check(lm is not None, "the resource must have a Last-Modified header", g)
    ts = parse_http_date(lm)

    step(f"{method} with an If-Unmodified-Since value BEFORE the last change: the "
         "precondition fails (412) and the feature is unchanged")
    r1 = rq(method, feat_url(fid), body, ctype,
            headers={"If-Unmodified-Since": http_date(ts - timedelta(days=1))})
    check(r1.status == 412,
          f"{method} with If-Unmodified-Since before the Last-Modified value must return 412", r1)
    g1 = get_feature(fid)
    check(g1.json().get("properties", {}).get("name") == name_before,
          "the resource must be unchanged after the 412 response")

    step(f"{method} with the current Last-Modified value: the precondition is met, "
         "the operation is executed and the response has a new Last-Modified value")
    r2 = rq(method, feat_url(fid), body, ctype,
            headers={"If-Unmodified-Since": http_date(ts)})
    if not queued(r2):
        check(r2.status in (200, 204),
              f"{method} with If-Unmodified-Since = Last-Modified must return 200 or 204", r2)
        lm2 = r2.header("Last-Modified")
        check(lm2 is not None,
              f"the successful {method} response must include a Last-Modified header", r2)
        check(parse_http_date(lm2) >= ts,
              f"the new Last-Modified value ({lm2}) must not be before the old value ({lm})")

    step(f"{method} without an If-Unmodified-Since header: the server either "
         "requires the precondition (428 or 409) or executes the operation")
    r3 = rq(method, feat_url(fid), body, ctype)
    check(r3.status in (428, 409) or 200 <= r3.status < 300,
          f"{method} without a conditional header must return 428, 409 or 2xx", r3)
    note(f"unconditional {method} on a timestamp-locked resource returns {r3.status} "
         f"({'server requires conditional requests' if r3.status in (428, 409) else 'permitted per /per/optimistic-locking-timestamps/ifunmodifiedsince-missing'})")


@ats("optimistic-locking-timestamps", "replace",
     "Conditional REPLACE operations using If-Unmodified-Since")
def test_olt_replace():
    _olt_conditional("PUT", "B.2", DATA["replace-building.json"], GEOJSON)


@ats("optimistic-locking-timestamps", "update",
     "Conditional UPDATE operations using If-Unmodified-Since")
def test_olt_update():
    if not declares("update"):
        raise Skip('the conformance declaration does not include the Conformance Class "Update"')
    _olt_conditional("PATCH", "B.3", DATA["update-building.json"], MERGE_PATCH)


@ats("optimistic-locking-timestamps", "delete",
     "Conditional DELETE operations using If-Unmodified-Since")
def test_olt_delete():
    step("GET the feature to obtain its Last-Modified value for the preconditions")
    g = get_feature("B.1")
    check(g.status == 200, "GET before the conditional DELETE requests must return 200", g)
    lm = g.header("Last-Modified")
    check(lm is not None, "the resource must have a Last-Modified header", g)
    ts = parse_http_date(lm)
    step("DELETE with an If-Unmodified-Since value BEFORE the last change: the "
         "precondition fails (412) and the feature is not removed")
    r1 = rq("DELETE", feat_url("B.1"),
            headers={"If-Unmodified-Since": http_date(ts - timedelta(days=1))})
    check(r1.status == 412,
          "DELETE with If-Unmodified-Since before the Last-Modified value must return 412", r1)
    check(get_feature("B.1").status == 200,
          "the resource must not have been removed after the 412 response")
    step("DELETE with the current Last-Modified value: the precondition is met and "
         "the feature is removed")
    r2 = rq("DELETE", feat_url("B.1"), headers={"If-Unmodified-Since": http_date(ts)})
    if not queued(r2):
        check(r2.status in (200, 204),
              "DELETE with If-Unmodified-Since = Last-Modified must return 200 or 204", r2)
        check(get_feature("B.1").status == 404, "GET after DELETE must return 404")
    step("DELETE another feature without an If-Unmodified-Since header: the server "
         "either requires the precondition (428 or 409) or executes the operation")
    r3 = rq("DELETE", feat_url("B.2"))
    check(r3.status in (428, 409) or 200 <= r3.status < 300,
          "DELETE without a conditional header must return 428, 409 or 2xx", r3)


# =====================================================================
# Conformance Class "Optimistic Locking using ETags"
# =====================================================================

@ats("optimistic-locking-etags", "get-etag",
     "Resource representations include an ETag header")
def test_ole_get():
    for fid in list_ids():
        step("GET the feature: the response has an ETag header with a valid "
             "entity tag")
        r = get_feature(fid)
        check(r.status == 200, f"GET {feat_url(fid)} must return 200", r)
        etag = r.header("ETag")
        check(etag is not None, f"the response for {fid} must include an ETag header", r)
        check(re.match(r'^(W/)?"[^"]*"$', etag), f"'{etag}' is not a valid entity tag")


def _ole_conditional(method, fid, body, ctype):
    step("GET the feature to obtain its entity tag for the preconditions")
    g = get_feature(fid)
    check(g.status == 200, "GET before the conditional requests must return 200", g)
    name_before = g.json().get("properties", {}).get("name")
    etag = g.header("ETag")
    check(etag is not None, "the resource must have an ETag header", g)

    step(f"{method} with a non-matching If-Match entity tag: the precondition "
         "fails (412) and the feature is unchanged")
    r1 = rq(method, feat_url(fid), body, ctype, headers={"If-Match": '"0"'})
    check(r1.status == 412, f"{method} with a non-matching If-Match must return 412", r1)
    g1 = get_feature(fid)
    check(g1.json().get("properties", {}).get("name") == name_before,
          "the resource must be unchanged after the 412 response")

    step(f"{method} with the current entity tag: the precondition is met, the "
         "operation is executed and the response has a new entity tag")
    r2 = rq(method, feat_url(fid), body, ctype, headers={"If-Match": etag})
    if not queued(r2):
        check(r2.status in (200, 204),
              f"{method} with a matching If-Match must return 200 or 204", r2)
        etag2 = r2.header("ETag")
        check(etag2 is not None,
              f"the successful {method} response must include an ETag header", r2)
        check(etag2 != etag, "the new entity tag must differ from the old one")

    step(f"{method} without an If-Match header: the server either requires the "
         "precondition (428 or 409) or executes the operation")
    r3 = rq(method, feat_url(fid), body, ctype)
    check(r3.status in (428, 409) or 200 <= r3.status < 300,
          f"{method} without a conditional header must return 428, 409 or 2xx", r3)


@ats("optimistic-locking-etags", "replace",
     "Conditional REPLACE operations using If-Match")
def test_ole_replace():
    _ole_conditional("PUT", "B.2", DATA["replace-building.json"], GEOJSON)


@ats("optimistic-locking-etags", "update",
     "Conditional UPDATE operations using If-Match")
def test_ole_update():
    if not declares("update"):
        raise Skip('the conformance declaration does not include the Conformance Class "Update"')
    _ole_conditional("PATCH", "B.3", DATA["update-building.json"], MERGE_PATCH)


@ats("optimistic-locking-etags", "delete",
     "Conditional DELETE operations using If-Match")
def test_ole_delete():
    step("GET the feature to obtain its entity tag for the preconditions")
    g = get_feature("B.1")
    check(g.status == 200, "GET before the conditional DELETE requests must return 200", g)
    etag = g.header("ETag")
    check(etag is not None, "the resource must have an ETag header", g)
    step("DELETE with a non-matching If-Match entity tag: the precondition fails "
         "(412) and the feature is not removed")
    r1 = rq("DELETE", feat_url("B.1"), headers={"If-Match": '"0"'})
    check(r1.status == 412, "DELETE with a non-matching If-Match must return 412", r1)
    check(get_feature("B.1").status == 200,
          "the resource must not have been removed after the 412 response")
    step("DELETE with the current entity tag: the precondition is met and the "
         "feature is removed")
    r2 = rq("DELETE", feat_url("B.1"), headers={"If-Match": etag})
    if not queued(r2):
        check(r2.status in (200, 204), "DELETE with a matching If-Match must return 200 or 204", r2)
        check(get_feature("B.1").status == 404, "GET after DELETE must return 404")
    step("DELETE another feature without an If-Match header: the server either "
         "requires the precondition (428 or 409) or executes the operation")
    r3 = rq("DELETE", feat_url("B.2"))
    check(r3.status in (428, 409) or 200 <= r3.status < 300,
          "DELETE without a conditional header must return 428, 409 or 2xx", r3)


# =====================================================================
# Conformance Class "Handling Preference"
# =====================================================================

@ats("handling", "prefer",
     "The server supports the handling preference")
def test_hdl_prefer():
    body = DATA["create-building.json"]
    for prefer in (None, "handling=strict", "handling=lenient"):
        hdrs = {"Prefer": prefer} if prefer else None
        step("POST a valid feature " + (f"with 'Prefer: {prefer}'" if prefer
             else "without a Prefer header") + ": the server accepts the "
             "preference and processes the request (2xx)")
        r = rq("POST", items_url(), body, GEOJSON, headers=hdrs)
        check(200 <= r.status < 300,
              f"POST with a valid body {'and Prefer: ' + prefer if prefer else 'without a Prefer header'} "
              f"must return 2xx", r)


@ats("handling", "strict",
     "Strict handling rejects request bodies that do not conform to published constraints")
def test_hdl_strict():
    ids_before = list_ids()
    step("POST a feature that violates a published constraint with "
         "'Prefer: handling=strict': the request is rejected (4xx) with error "
         "information and nothing is created")
    r = rq("POST", items_url(), DATA["create-building-invalid.json"], GEOJSON,
           headers={"Prefer": "handling=strict"})
    check(400 <= r.status < 500,
          "POST with an invalid body and Prefer: handling=strict must be rejected with a 4xx status code", r)
    check(len(r.body) > 0, "the response content must include information about the error condition", r)
    check(list_ids() == ids_before, "the resource must not have been created")
    STATE["strict-response"] = r


@ats("handling", "lenient",
     "Lenient handling is at least as permissive as the default handling")
def test_hdl_lenient():
    for key in ("create-building.json", "create-building-invalid.json"):
        step(f"POST {key} without a Prefer header: the reference behaviour for "
             "the comparison with lenient handling")
        r1 = rq("POST", items_url(), DATA[key], GEOJSON)
        step(f"POST the same body ({key}) with 'Prefer: handling=lenient': lenient "
             "handling is at least as permissive as the default handling")
        r2 = rq("POST", items_url(), DATA[key], GEOJSON, headers={"Prefer": "handling=lenient"})
        if 200 <= r1.status < 300:
            check(200 <= r2.status < 300,
                  f"POST ({key}) with Prefer: handling=lenient must succeed if the same request "
                  f"without the header succeeds", r2)
        else:
            note(f"lenient: request without Prefer header returned {r1.status} for {key} — "
                 "assertion skipped for this body")


@ats("handling", "preference-applied",
     "Responses declare the applied handling preference")
def test_hdl_preference_applied():
    r = STATE.get("strict-response")
    if r is None:
        step("POST an invalid feature with 'Prefer: handling=strict': the "
             "rejection response declares the applied preference in the "
             "Preference-Applied header")
        r = rq("POST", items_url(), DATA["create-building-invalid.json"], GEOJSON,
               headers={"Prefer": "handling=strict"})
    if not (400 <= r.status < 500):
        raise Skip("the strict request was not rejected, the preference was not applied")
    pa = r.header("Preference-Applied")
    check(pa is not None, "the response must include a Preference-Applied header", r)
    check("handling=strict" in pa.replace(" ", ""),
          f"the Preference-Applied header must be 'handling=strict', got '{pa}'")


# =====================================================================
# Conformance Class "Features"
# =====================================================================

@ats("features", "endpoints",
     "Mutable features are the features of the feature collections of the API")
def test_feat_endpoints():
    step("GET the collections: the mutable feature collections are collections of "
         "the API")
    r = rq("GET", f"{CFG.landing_page}/collections", accept="application/json")
    check(r.status == 200, "GET {landingPageUri}/collections must return 200", r)
    colls = [c for c in r.json().get("collections", [])
             if c.get("itemType") in (None, "feature")]
    match = [c for c in colls if c.get("id") == CFG.collection]
    check(match, f"the mutable feature collection '{CFG.collection}' must be one of the collections")
    ids = list_ids()
    check(ids, "the resources endpoint {landingPageUri}/collections/{collectionId}/items "
               "must provide the features")
    for fid in ids:
        g = get_feature(fid)
        check(g.status == 200,
              "each feature must have the resource endpoint "
              "{landingPageUri}/collections/{collectionId}/items/{featureId}", g)


@ats("features", "put-create",
     "Support for creating features using PUT is declared in the collection")
def test_feat_put_create():
    """The condition is a mutable feature collection that supports creating new
    features with PUT; --put-create-collection names it (test parameter)."""
    coll = CFG.put_create_collection
    if not coll:
        step("PUT to a non-existing feature: determine whether the collection "
             "supports creating features with PUT (condition of the test)")
        r = rq("PUT", feat_url("B.902"), DATA["create-building.json"], GEOJSON,
               headers=precond_headers())
        if r.status not in (201, 202):
            raise Skip("no mutable feature collection supports creating new features "
                       "using PUT (see --put-create-collection)")
    else:
        step(f"[{coll}] PUT to a non-existing feature: the feature is created "
             "(201) with the identifier from the request URI")
        r = rq("PUT", feat_url("B.902", coll), DATA["create-building.json"], GEOJSON)
        check(r.status in (201, 202),
              f"[{coll}] PUT to a non-existing feature must return 201 (or 202, if the "
              "operation has been queued for processing)", r)
        if r.status != 202:
            g = get_feature("B.902", coll)
            check(g.status == 200, f"[{coll}] GET of the created feature must return 200", g)
            check(g.json().get("id") == "B.902",
                  "the new feature must have the identifier from the request URI, "
                  f"got {g.json().get('id')!r}")
    label = coll or CFG.collection
    step("GET the collections: the collection declares "
         "'supportsNonAutogeneratedResourceIds': true")
    r = rq("GET", f"{CFG.landing_page}/collections", accept="application/json")
    entry = [c for c in r.json().get("collections", []) if c.get("id") == label]
    check(entry and entry[0].get("supportsNonAutogeneratedResourceIds") is True,
          f"the collection {label} in /collections must include "
          "supportsNonAutogeneratedResourceIds: true")
    check(collection_doc(coll).get("supportsNonAutogeneratedResourceIds") is True,
          f"the collection resource {label} must include "
          "supportsNonAutogeneratedResourceIds: true")


@ats("features", "crs84",
     "Geometries are interpreted as WGS 84, if CRS support is not implemented")
def test_feat_crs84():
    if declares("crs"):
        raise Skip('the conformance declaration includes the Conformance Class '
                   '"Coordinate Reference Systems by Reference"')
    body = DATA["create-building.json"]
    step("POST a feature with WGS 84 coordinates and no Content-Crs header: the "
         "coordinates are interpreted as CRS84")
    r1 = rq("POST", items_url(), body, GEOJSON)
    check(r1.status in (201, 202), "POST must be processed successfully", r1)
    if r1.status == 201:
        step("GET the new feature: its geometry is unchanged")
        g = rq("GET", location_of(r1), accept=ACCEPT_FEATURE)
        check(g.status == 200, "GET of the new feature must return 200", g)
        check(geom_eq(body["geometry"], g.json().get("geometry")),
              "the geometry must be unchanged (interpreted as WGS 84 longitude/latitude)")
    step("POST with a Content-Crs header for another CRS: the request is rejected, "
         "because the API does not support other coordinate reference systems")
    r2 = rq("POST", items_url(), body, GEOJSON,
            headers={"Content-Crs": "<http://www.opengis.net/def/crs/EPSG/0/25832>"})
    check(400 <= r2.status < 500,
          "POST with a Content-Crs header other than CRS84 must be rejected", r2)


@ats("features", "crs",
     "Geometries are interpreted in the declared coordinate reference system")
def test_feat_crs():
    if not declares("crs"):
        raise Skip('the conformance declaration does not include the Conformance Class '
                   '"Coordinate Reference Systems by Reference"')
    coll = collection_doc()
    crs_list = collection_crs_list(coll)
    other = [c for c in crs_list if "CRS84" not in c]
    if not other:
        raise Skip("the collection does not support a coordinate reference system other than the default CRS")
    crs = next((c for c in other if c.endswith("/25832")), other[0])
    body = DATA["create-building.json"]

    step("POST a feature without a Content-Crs header: the coordinates are "
         "interpreted in the default CRS of the collection")
    r1 = rq("POST", items_url(), body, GEOJSON)
    check(r1.status == 201, "the first POST (default CRS) must be processed successfully", r1)
    loc1 = location_of(r1)
    step(f"GET the new feature with crs={crs}: the geometry converted to that CRS "
         "is the reference for the next request")
    g1 = rq("GET", f"{loc1}?crs={quote(crs, safe='')}", accept=ACCEPT_FEATURE)
    check(g1.status == 200, f"GET with crs={crs} must return 200", g1)
    geom_crs = g1.json().get("geometry")
    check(geom_crs is not None, "the feature must have a geometry in the requested CRS")

    body2 = dict(body)
    body2["geometry"] = geom_crs
    step(f"POST the same location with coordinates in {crs} and a matching "
         "Content-Crs header: the declared CRS is honoured")
    r2 = rq("POST", items_url(), body2, GEOJSON,
            headers={"Content-Crs": f"<{crs}>"})
    check(r2.status == 201, "the second POST (converted coordinates, Content-Crs header) "
                            "must be processed successfully", r2)
    loc2 = location_of(r2)
    step("GET the second feature in the same CRS: both features represent the "
         "same location")
    g2 = rq("GET", f"{loc2}?crs={quote(crs, safe='')}", accept=ACCEPT_FEATURE)
    check(g2.status == 200, f"GET with crs={crs} must return 200", g2)
    check(geom_eq(g1.json().get("geometry"), g2.json().get("geometry"), tol=0.05),
          "both features must have geometries that represent the same location "
          f"(within the conversion accuracy): {json.dumps(g2.json().get('geometry'))[:200]}")

    unsupported = next(c for c in (
        "http://www.opengis.net/def/crs/EPSG/0/26910",
        "http://www.opengis.net/def/crs/EPSG/0/27700") if c not in crs_list)
    step("POST with a Content-Crs header for a CRS that the collection does not "
         "support: the request is rejected")
    r3 = rq("POST", items_url(), body, GEOJSON, headers={"Content-Crs": f"<{unsupported}>"})
    check(400 <= r3.status < 500,
          "POST with an unsupported CRS in the Content-Crs header must be rejected", r3)


@ats("features", "gml-srsname",
     "The srsName attribute in GML request bodies is honored")
def test_feat_gml_srsname():
    if not declares("crs"):
        raise Skip('the conformance declaration does not include the Conformance Class '
                   '"Coordinate Reference Systems by Reference"')
    if not (declares("gmlsf0") or declares("gmlsf2")):
        raise Skip("the conformance declaration does not include a GML conformance class")
    if "create-building.gml" not in DATA:
        raise Skip("no GML representation of the test dataset is available (test parameter)")
    body = DATA["create-building.gml"]
    crs = re.search(r'srsName="([^"]*)"', body).group(1)
    step("POST a GML feature whose geometry declares another CRS in the srsName "
         "attribute: the attribute is honoured")
    r = rq("POST", items_url(), body.encode(), GML)
    if r.status == 415:
        raise Skip("the collection does not support the CREATE operation with GML")
    check(r.status in (201, 202), "POST with a GML feature must be processed successfully", r)
    if r.status == 202:
        return
    loc = location_of(r)
    step(f"GET the new feature with crs={crs}: the geometry is the submitted one")
    g = rq("GET", f"{loc}?crs={quote(crs, safe='')}", accept=ACCEPT_FEATURE)
    check(g.status == 200, f"GET with crs={crs} must return 200", g)
    # the GML file mirrors the JSON-FG file: the same polygon in EPSG:25832
    expected = DATA["create-building-jsonfg.json"]["place"]["coordinates"]
    geom = g.json().get("geometry")
    check(geom is not None and geom.get("type") == "Polygon" and
          num_eq(geom.get("coordinates"), expected, 0.05),
          "the geometry must be identical within the coordinate conversion accuracy "
          f"(the srsName attribute has been honored), got {json.dumps(geom)[:200]}")


@ats("features", "schema",
     "Mutation requests are processed according to the published schema")
def test_feat_schema():
    if not declares("schemas"):
        raise Skip('the conformance declaration does not include the Conformance Class '
                   '"Returnables and Receivables"')
    url = f"{CFG.landing_page}/collections/{CFG.collection}/schema"
    step("GET the schema of the collection: it is a JSON Schema")
    r = rq("GET", url, accept=SCHEMA_JSON)
    check(r.status == 200, f"GET {url} must return 200", r)
    schema = r.json()
    check(isinstance(schema, dict) and ("properties" in schema or "$schema" in schema),
          "the response content must be a JSON Schema")
    STATE["schema"] = schema

    step("POST a feature that meets the schema constraints: it is accepted")
    r1 = rq("POST", items_url(), DATA["create-building.json"], GEOJSON)
    check(r1.status in (201, 202), "POST with a schema-conformant feature must be processed successfully", r1)

    no_additional = schema.get("additionalProperties") is False
    body = json.loads(json.dumps(DATA["create-building.json"]))
    body["properties"]["additionalProperty"] = "additional value"
    step("POST the feature with an additional property that the schema does not "
         "specify: " + ("the request is rejected, because the schema states "
                        "'additionalProperties': false" if no_additional else
                        "it is not rejected because of that property"))
    r2 = rq("POST", items_url(), body, GEOJSON)
    if no_additional:
        check(400 <= r2.status < 500,
              "a POST request with a property that is not specified in the schema "
              "must be rejected, because the schema states "
              "\"additionalProperties\": false", r2)
    else:
        check(200 <= r2.status < 300,
              "a POST request must not be rejected because of an additional property "
              "that is not specified in the schema", r2)
        note("schema: the schema does not state \"additionalProperties\": false, so "
             "the additional property must not be a reason to reject the request")

    # a property that the schema specifies as read-only must not be set (provision E)
    read_only = [k for k, v in (schema.get("properties") or {}).items()
                 if isinstance(v, dict) and v.get("readOnly") is True
                 and v.get("x-ogc-role") != "id"]
    if not read_only:
        note("schema: the schema specifies no read-only property besides the "
             "identifier, so the assertion about read-only properties is skipped")
        return
    prop = read_only[0]
    body = json.loads(json.dumps(DATA["create-building.json"]))
    body["properties"][prop] = "2020-01-01T00:00:00Z" if "date" in str(
        (schema["properties"][prop]).get("format")) else "any value"
    step(f"POST the feature with the read-only property '{prop}': the request is "
         "rejected, because a read-only property must not be set")
    r3 = rq("POST", items_url(), body, GEOJSON)
    check(400 <= r3.status < 500,
          f"a POST request that sets the read-only property '{prop}' must be "
          "rejected", r3)


@ats("features", "geojson",
     "GeoJSON representations in mutation requests are processed correctly")
def test_feat_geojson():
    if not declares("geojson"):
        raise Skip('the conformance declaration does not include the Conformance Class "GeoJSON"')
    if not declares("schemas"):
        raise Skip('the conformance declaration does not include the Conformance Class '
                   '"Returnables and Receivables"')
    body = dict(DATA["replace-building.json"])
    body["id"] = "B.999"
    step("PUT a GeoJSON feature with an 'id' member that differs from the feature "
         "identifier: the member is ignored and the geometry is mapped to the "
         "primary geometry (or the request is rejected)")
    r = mutate("PUT", feat_url("B.2"), body, GEOJSON, fid="B.2")
    if r.status == 415:
        raise Skip("the collection does not support application/geo+json in REPLACE "
                   "requests (415)")
    if 400 <= r.status < 500:
        g = get_feature("B.2")
        check(g.json().get("properties", {}).get("name") == "Old Mill",
              "the feature must be unchanged after the rejection")
        note(f"geojson: PUT with an 'id' member rejected with {r.status} (permitted)")
        return
    check(r.status in (200, 204, 202), "PUT must be processed successfully or rejected with 4xx", r)
    if r.status == 202:
        return
    g = get_feature("B.2")
    check(g.status == 200, "GET after REPLACE must return 200", g)
    f = g.json()
    check(f.get("id") == "B.2", "the 'id' member in the request body must be ignored")
    check(geom_eq(body["geometry"], f.get("geometry")),
          "the 'geometry' member must be mapped to the property with the role 'primary-geometry'")


@ats("features", "json-merge-patch",
     "UPDATE requests with JSON Merge Patch documents are processed correctly")
def test_feat_json_merge_patch():
    if not declares("update"):
        raise Skip('the conformance declaration does not include the Conformance Class "Update"')
    if not supports_media_type(MERGE_PATCH, "UPDATE"):
        raise Skip("the collection does not support application/merge-patch+json in "
                   "UPDATE requests (Accept-Patch header of the OPTIONS response)")
    if not declares("schemas"):
        raise Skip('the conformance declaration does not include the Conformance Class '
                   '"Returnables and Receivables"')
    patch = DATA["update-building.json"]
    step("PATCH a JSON Merge Patch document: one property is changed, one added, "
         "one removed with null, and the primary geometry is replaced")
    r = mutate("PATCH", feat_url("B.3"), patch, MERGE_PATCH, fid="B.3")
    if not queued(r):
        check(r.status in (200, 204), "PATCH with a JSON Merge Patch document must be processed successfully", r)
        g = get_feature("B.3")
        check(g.status == 200, "GET after UPDATE must return 200", g)
        f = g.json()
        props = f.get("properties", {})
        check(num_eq(props.get("height"), 7.8, 1e-6),
              f"the changed property must have the new value, got height={props.get('height')!r}")
        check(props.get("owner") == "Jane Doe",
              f"the added property must be present, got owner={props.get('owner')!r}")
        check(props.get("name") is None,
              f"the property with the null value must be unset, got name={props.get('name')!r}")
        check(geom_eq(patch["geometry"], f.get("geometry")),
              "the primary geometry must be the geometry submitted in the request body")
    step("PATCH a document that changes the property with the role 'id': the "
         "request is rejected")
    r2 = mutate("PATCH", feat_url("B.3"), {"id": "B.888"}, MERGE_PATCH, fid="B.3")
    check(400 <= r2.status < 500,
          "a JSON Merge Patch document that changes the property with the role 'id' "
          "must be rejected with a 4xx status code", r2)


@ats("features", "jsonfg",
     "JSON-FG extensions in GeoJSON request bodies are supported")
def test_feat_jsonfg():
    if not declares("geojson"):
        raise Skip('the conformance declaration does not include the Conformance Class "GeoJSON"')
    if not declares("jsonfg-api"):
        raise Skip('the conformance declaration does not include the Conformance Class '
                   '"JSON-FG in Web APIs"')
    step("POST a GeoJSON feature with a profile link for 'rfc7946': plain GeoJSON "
         "is accepted")
    r1 = rq("POST", items_url(), DATA["create-building.json"], GEOJSON,
            headers={"Link": f"<{PROFILE_RFC7946}>; rel=profile"})
    check(r1.status in (201, 202),
          "POST with a GeoJSON feature and the rfc7946 profile link must be processed successfully", r1)

    body = DATA["create-building-jsonfg.json"]
    step("POST a feature with JSON-FG extensions and a profile link for 'jsonfg': "
         "the geometry in the 'place' member is processed according to JSON-FG")
    r2 = rq("POST", items_url(), body, GEOJSON,
            headers={"Link": f"<{PROFILE_JSONFG}>; rel=profile"})
    check(r2.status in (201, 202),
          "POST with a JSON-FG feature and the jsonfg profile link must be processed successfully", r2)
    if r2.status == 202:
        return
    loc2 = location_of(r2)

    place_crs = body["place"]["coordRefSys"]
    candidates = [f"{loc2}?profile=jsonfg", f"{loc2}?f=jsonfg"]
    if declares("crs"):
        candidates = [c + f"&crs={quote(place_crs, safe='')}" for c in candidates]
    g, place = None, None
    for url in candidates:
        step("GET the new feature in the JSON-FG profile: the 'place' member is "
             "the submitted geometry")
        g = rq("GET", url, accept=ACCEPT_FEATURE)
        if g.status == 200:
            try:
                place = g.json().get("place")
            except Fail:
                place = None
            if place is not None:
                note(f"jsonfg: JSON-FG representation retrieved via {url.split('?')[1].split('&')[0]}")
                break
    check(g is not None and g.status == 200, "GET of the new feature requesting the JSON-FG profile must return 200", g)
    check(place is not None, "the JSON-FG representation must include a 'place' member", g)
    if declares("crs"):
        check(place.get("type") == body["place"]["type"] and
              num_eq(place.get("coordinates"), body["place"]["coordinates"], 0.05),
              f"the 'place' member must represent the geometry submitted in the request body, "
              f"got {json.dumps(place)[:200]}")
    else:
        note("jsonfg: CRS support not declared — the place geometry is compared by type only")
        check(place.get("type") == body["place"]["type"],
              "the 'place' member must represent the submitted geometry")


@ats("features", "gml",
     "GML representations in mutation requests are processed correctly")
def test_feat_gml():
    if not (declares("gmlsf0") or declares("gmlsf2")):
        raise Skip("the conformance declaration does not include a GML conformance class")
    if "replace-building.gml" not in DATA:
        raise Skip("no GML representation of the test dataset is available (test parameter)")
    pre = get_feature("B.2")
    check(pre.status == 200, "GET before REPLACE must return 200", pre)
    name_before = pre.json().get("properties", {}).get("name")
    body = DATA["replace-building.gml"]
    body = re.sub(r'gml:id="[^"]*"', 'gml:id="B.998"', body, count=1)
    body = re.sub(r"(<(?:\w+:)?name>)[^<]*(</(?:\w+:)?name>)",
                  r"\g<1>GML Replacement\g<2>", body, count=1)
    step("PUT a GML feature with a @gml:id attribute that differs from the feature "
         "identifier: the attribute is ignored (or the request is rejected)")
    r = mutate("PUT", feat_url("B.2"), body.encode(), GML, fid="B.2")
    if r.status == 415:
        raise Skip("the collection does not support the REPLACE operation with GML")
    if queued(r):
        return
    if 400 <= r.status < 500:
        g = get_feature("B.2")
        check(g.json().get("properties", {}).get("name") == name_before,
              "the feature must be unchanged after the rejection")
        note(f"gml: PUT with a differing @gml:id rejected with {r.status} (permitted)")
        return
    check(r.status in (200, 204), "PUT must be processed successfully or rejected with 4xx", r)
    g = get_feature("B.2")
    check(g.status == 200, "GET after REPLACE must return 200", g)
    f = g.json()
    check(f.get("id") == "B.2", "the @gml:id attribute in the request body must be ignored")
    check(f.get("properties", {}).get("name") == "GML Replacement",
          "the feature must have the new content submitted in the request body")


# ------------------------------------------------------------------ main

CLASS_LABELS = {
    "create-replace-delete": 'Conformance Class "Create/Replace/Delete"',
    "update": 'Conformance Class "Update"',
    "optimistic-locking-timestamps": 'Conformance Class "Optimistic Locking using Timestamps"',
    "optimistic-locking-etags": 'Conformance Class "Optimistic Locking using ETags"',
    "handling": 'Conformance Class "Handling Preference"',
    "features": 'Conformance Class "Features"',
}


def reset_dataset():
    if not CFG.reset_cmd:
        return
    p = subprocess.run(CFG.reset_cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"  WARNING: reset command failed: {p.stderr.strip()[:300]}", file=sys.stderr)
    time.sleep(0.3)


def main():
    global CFG, CONFORMS
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--landing-page", required=True, help="landing page URI of the Web API under test")
    ap.add_argument("--collection", default="buildings", help="collection id of the test dataset")
    ap.add_argument("--data-dir",
                    default=os.path.join(os.path.dirname(__file__), "..", "..", "standard", "data"),
                    help="directory with the test dataset files "
                         "(default: the standard/data directory of this standard)")
    ap.add_argument("--put-create-collection", default=None, metavar="COLLECTION",
                    help="collection id of a mutable feature collection that supports "
                         "creating new features with PUT (client-assigned identifiers)")
    ap.add_argument("--reset-cmd", default=None,
                    help="shell command that resets the test dataset (run before each conformance class)")
    ap.add_argument("--assume", action="append", default=[], metavar="KEY",
                    help="treat a conformance class as declared even if it is not, "
                         "for example to test an implementation that declares "
                         "pre-publication URIs "
                         f"(keys: {', '.join(CONF)})")
    ap.add_argument("--only", default=None, help="run only tests whose id contains this substring")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--verbose", action="store_true")
    CFG = ap.parse_args()
    CFG.landing_page = CFG.landing_page.rstrip("/")

    for name in ("create-building.json", "create-building-invalid.json",
                 "create-building-jsonfg.json", "replace-building.json",
                 "update-building.json"):
        with open(os.path.join(CFG.data_dir, name)) as f:
            DATA[name] = json.load(f)
    for name in ("create-building.gml", "replace-building.gml"):
        path = os.path.join(CFG.data_dir, name)
        if os.path.exists(path):
            with open(path) as f:
                DATA[name] = f.read()

    r = rq("GET", f"{CFG.landing_page}/conformance", accept="application/json")
    if r.status != 200:
        print(f"FATAL: GET {CFG.landing_page}/conformance returned {r.status}", file=sys.stderr)
        return 2
    CONFORMS = r.json().get("conformsTo", [])
    print(f"API under test: {CFG.landing_page}")
    print(f"Declared conformance classes ({len(CONFORMS)}):")
    for uri in CONFORMS:
        print(f"  {uri}")
    print()

    results = []
    current_class = None
    class_enabled = False
    for cls, name, fn, purpose in TESTS:
        test_id = f"/conf/{cls}/{name}"
        if CFG.only and CFG.only not in test_id:
            continue
        if cls != current_class:
            current_class = cls
            class_enabled = declares(cls)
            extra = "" if declares(cls) or cls not in CFG.assume else " (assumed via --assume)"
            print(f"== {CLASS_LABELS[cls]} — "
                  f"{'declared' if class_enabled else 'NOT declared, tests skipped'}{extra} ==")
            if class_enabled:
                reset_dataset()
        if not class_enabled:
            results.append((test_id, "SKIP", "conformance class not declared"))
            print(f"  SKIP {test_id}")
            continue
        if CFG.verbose:
            print(f"  ---- {test_id}: {purpose}")
        try:
            fn()
            results.append((test_id, "PASS", ""))
            print(f"  PASS {test_id}")
        except Skip as e:
            results.append((test_id, "SKIP", str(e)))
            print(f"  SKIP {test_id}\n       condition not met: {e}")
        except Fail as e:
            results.append((test_id, "FAIL", str(e)))
            print(f"  FAIL {test_id}\n       {e}")
        except Exception as e:  # noqa: BLE001
            results.append((test_id, "ERROR", f"{type(e).__name__}: {e}"))
            print(f"  ERROR {test_id}\n       {type(e).__name__}: {e}")

    print()
    n = {s: sum(1 for _, st, _ in results if st == s) for s in ("PASS", "FAIL", "ERROR", "SKIP")}
    print(f"Summary: {n['PASS']} passed, {n['FAIL']} failed, {n['ERROR']} errors, "
          f"{n['SKIP']} skipped (of {len(results)} tests)")
    for test_id, status, msg in results:
        if status in ("FAIL", "ERROR"):
            print(f"  {status} {test_id}: {msg[:200]}")
    return 1 if (n["FAIL"] or n["ERROR"]) else 0


if __name__ == "__main__":
    sys.exit(main())
