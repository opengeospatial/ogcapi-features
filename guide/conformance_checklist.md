__WFS3 Core Conformance Checklist__

Derived from the [WFS3 spec](https://rawgit.com/opengeospatial/WFS_FES/master/docs/17-069.html#_requirement_class_core) as of 2018-03-15.

**CAUTION: This needs to be updated in a few places to the first draft release.**

- (recommended) checkboxes aren't strictly necessary for conformance
- (optional) checkboxes have value but may be ignored without problem

**7.2** API landing page
* [ ] GET request at **/** served
* [ ] Response content is based on [root.yaml](https://raw.githubusercontent.com/opengeospatial/WFS_FES/master/core/openapi/schemas/root.yaml) and minimally includes links to:
    * [ ] **/api**
    * [ ] **/conformance**
    * [ ] **/collections**

**7.3** API Definition
* [ ] GET request at **/api** served
* [ ] Response content is the api definition document
* [ ] (recommended) Response content is OpenAPI format
* If multiple formats are provided, use content negotiation

**7.4** Declaration of conformance classes
* [ ] GET request at **/conformance** served
* [ ] Resonse content is based on OpenAPI schema [req-classes.yaml](https://raw.githubusercontent.com/opengeospatial/WFS_FES/master/core/openapi/schemas/req-classes.yaml).
  * [ ] conformsTo in response contains
    * [ ] http://www.opengis.net/spec/wfs-1/3.0/req/core
    * [ ] (recommended) http://www.opengis.net/spec/wfs-1/3.0/req/html
    * [ ] (recommended) http://www.opengis.net/spec/wfs-1/3.0/req/geojson

**7.5** HTTP 1.1
* [ ] Conforms to [HTTP 1.1](https://rawgit.com/opengeospatial/WFS_FES/master/docs/17-069.html#rfc2616), including correct use of status codes, headers, etc.
* [ ] (recommended) Supports [entity tags](https://rawgit.com/opengeospatial/WFS_FES/master/docs/17-069.html#rfc2616)

**7.7** Support for cross-origin requests
* [ ] (recommended) If the server will be accessed from the browser, allow cross-origin requests.

**7.8** Encodings
* [ ] (recommended) HTML 1.1
* [ ] (recommended) GeoJSON
* See [Media Types](https://rawgit.com/opengeospatial/WFS_FES/master/docs/17-069.html#mediatypes) for guidance
* For multiple encodings, the server needs a mechanism to mint encoding-specific links, such as /my/url.geojson or /my/url?f=geojson

**7.9** Coordinate reference systems
* [ ] Geometries are served in WGS84 (EPSG/SRID 4326) unless another is requested.
* There is currently no mechanism to request another CRS.

**7.10** Link headers
* [ ] All links in response payloads are included as Link headers as well.

**7.11** Feature collection**s** metadata
* [ ] GET request at **/collections** served
* [ ] Response content based on [content.yaml](https://raw.githubusercontent.com/opengeospatial/WFS_FES/master/core/openapi/schemas/content.yaml)
* [ ] Response "links" property includes:
  * [ ] rel "self"
  * [ ] rel "alternate" for each additional encoding available
  * [ ] rel "item" for each collection available
  * [ ] All links include "rel"
  * [ ] All links include "type" specifying content type
  * [ ] (recommended) For each external link defining structure or semantics of data contained in collections, include a link w/ rel "describedBy"
  * [ ] For each supported encoding for each feature collection include an item with rel "item" in the "links" property.
* [ ] Response "collections" property includes an entry for each feature collection.
* [ ] If response provides an "extent" property it is formatted as a bounding box of the form [SWlong, SWlat, NElong, NElat]

**7.12** Feature collection metadata
* [ ] GET request at **/collections/{name}** served
* [ ] Response is metadata for the collection indicated using the same schema as in 7.11.

**7.13** Feature collections
* [ ] GET request at **/collections/{name}/items** served
  * [ ] "limit" querystring parameter indicating max number of features to provide at once.
    * [ ] "limit" parameter includes "minimum" with value 1
    * [ ] "limit" parameter includes (changeable) "default"
    * [ ] "limit" parameter includes (changeable) "maximum"
  * [ ] "bbox" querystring parameter.  Only features intersecting this rectangle are returned.
  * [ ] (recommended) For simple int/string properties of features include a querystring parameter with the property name to filter on.  For strings, wildcard matches may be useful in addition to simple equality.
* [ ] Response includes links:
  * [ ] rel "self"
  * [ ] rel "alternate", one for every other content type
  * [ ] (recommended) rel "next" for additional features beyond limit.
    * [ ] "next" link uses same rules for "limit"
  * [ ] (optional) rel "prev" to mirror functionality of "next"
  * [ ] all links include "ref" & "type"
* Heads-up: details for timeStamp, numberMatched, numberReturned parameters are in the works.

**7.14** Feature
* [ ] GET request at **/collections/{name}/items]{id}** served
* [ ] Response payload contains the feature identified.
* [ ] Response includes links:
  * [ ] rel "self"
  * [ ] rel "alternate" for other content types supported.
  * [ ] rel "collection"
