# Collection Summary

## Metadata

| Tag | Value |
| ---- | ---------------- |
| Proposal | [Summary](https://github.com/tschaub/ogcapi-features/tree/summary/proposals/002_Summary.md) |
| Authors | Various |
| Review Manager | TBD |
| Status | Draft |
| Implementations | None |
| Issues | None |
| Previous Revisions | None |

## Introduction

This proposal suggests that the spec define a `summary` resource (all names TBD) that describes a collection.  It may be that this information belongs in the existing collection info (e.g. at `/collections/{id}`), but for the purposes of this doc, we'll say it is going to be a new resource (e.g. at `/collections/{id}/summary`).

## Motivation

There are few motivations for this:

 * A client should have a way to get the formal schema for items in a collection if one exists.  The current suggestion to use a link with `rel="describedBy"` doesn't fully address this need since it doesn't provide a robust way for a client to get the schema for multiple content types (for example, if a service supports GML, KML, and GeoJSON output, the `type` and `rel` of a link is not enough information for a client to know which schema applies to which output format).

 * A "filter" extension should have a way to describe which properties are filterable and how clients should access a specific property in a filter expression.

 * A "search" extension should have a way to describe which properties can be used in sorting.

 * An "editing" extension should have a way to describe which properties are writeable (e.g. in an update) or might want to allow for a different schema for each method (e.g. one schema for create, one for update).

## Proposed solution

## Example

Here is an example of what this summary resource might look like for a "buildings" collection (e.g. at https://example.com/collections/buildings/summary)

```json
{
  "properties": {
    "application/geo+json": {
      "height": {
        "schema": {
          "href": "http://example.com/collections/buildings/schema#/definitions/height"
        }
      },
      "age": {
        "schema": {
          "href": "http://example.com/collections/foo/schema#/definitions/age"
        },
        "filter": {
          "allowed": false
        },
        "search": {
          "sortable": false
        }
      },
      "taxId": {
        "schema": {
          "href": "http://example.com/collections/foo/schema#/definitions/taxId"
        },
        "editing": {
          "writeable": false
        }
      }
    }
  }
}
```

Notes on the above example:

 * The properties of the `properties` object (ack!) are content types.  Using an object means that there will be one member per content type.  So it looks like the responses `content` object in OpenAPI 3.

 * The `schema` property would be defined by the core Features spec.  In the case of JSON schema, an href could deeply link to the spceific definition.  In the case of an XSD doc, there could be two properties: `href` and `path` (maybe?) so an XPath expression could be provided to refer to the part of the schema specific to a single property.

 * Individual extensions could add their own members to each of the properties object.  For example, the "filter" expression could define a `filter` object.
 
## Detailed design

TODO

## Backwards compatibility

This proposal doesn't introduce any breaking changes.

## Alternatives considered

In discussion with others here at the Features/STAC sprint, we discussed a few other alternatives.  This isn't a comprehensive set of notes, but we covered things like the list below:

### A new resource per extension

We considered the alternative that each extension would add its own resource at a new path.  For example, the filter extension might add a `/collections/buildings/queryables` resource.  Then the search extension might add a `/collections/buildings/sortables` resource.  And then the editing extension might add a `/collections/buildings/writeables` resource.  This began to feel unscalable and awkward for clients who want to get a complete picture of how to work with a collection.

### Additional properties in the existing schema

We didn't dig too far into this, but thought briefly about the idea of trying to extend the schema syntax to include more descriptive information for a property.  For example, a snippet of JSON schema might look like this:

```json
{
  "definitions": {
    "age": {
      "type": "number",
      "filterable": false,
      "sortable": false
    }
  }
}

Even if this were possible, our concern was that generic schema parsers would not expose these additional properties to a client.
