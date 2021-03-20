# OGC API - Features - Part n: Property Selection

This folder contains an outline for the "Property Selection" extension of the OGC API Features standard.

THIS IS CURRENTLY A PROPOSAL DRAFT.

By default, OGC API Features always returns the complete feature in a response. However, the client sometimes need only selected properties and a capability to restrict the response to the needed information can reduce the volume of data to be transmitted. Sample use cases:

- The client does not need the geometry and only wants to present a table with property information. This option is in particular relevant for line strings, polygons or solids with many coordinates.
- The client only needs a subset of the properties, e.g. for styling the features in a map. This option is in particular relevant for features with many properties.

The standard will define two requirements classes:

- "Property Selection" will specifies the following query parameters for the `/collections/{collectionId}/items` and `/collections/{collectionId}/items/{featureId}` endpoints:
  - `properties` (default: all properties): A string array with feature properties listed in the `returnables` schema that will be included in the response. Dependency: http://www.opengis.net/spec/ogcapi-features-n/1.0/req/schema.
    - For cases where properties are object-valued: Selecting the name/path of an object-values property will return the complete object. Selecting one or more properties inside the object will return only the selected properties.
  - `skip-geometry` (default: `false`): If `true` omit geometry properties from the response.
- "Property Selection (Features) will specify the requirements for implementations that support "Property Selection" and http://www.opengis.net/spec/ogcapi-features-1/1.0/req/core. The requirements apply only to collections with no `itemType` or with a value "feature".

For discussion: Do we also add another resource like `/collections/{collectionId}/ids` to just retrieve an array with the featureId values? The resource would accept all filtering query parameters of the `/collections/{collectionId}/items` endpoint (e.g. `bbox`, `datetime`, collection-specific filter parameters, `filter`, `filter-lang`, `filter-crs`).

## Example

https://demo.ldproxy.net/daraa/collections/CulturePnt/items?f=json&properties=F_CODE,ZI005_FNA&skipGeometry=true returns

```json
{
  "type": "FeatureCollection",
  "links": [
    {
      "href": "https://demo.ldproxy.net/daraa/collections/CulturePnt/items?properties=F_CODE%2CZI005_FNA&skipGeometry=true&f=json",
      "rel": "self",
      "type": "application/geo+json",
      "title": "This document"
    },
    {
      "href": "https://demo.ldproxy.net/daraa/collections/CulturePnt/items?properties=F_CODE%2CZI005_FNA&skipGeometry=true&f=html",
      "rel": "alternate",
      "type": "text/html",
      "title": "This document as HTML"
    }
  ],
  "numberReturned": 5,
  "numberMatched": 5,
  "timeStamp": "2021-03-20T10:12:01Z",
  "features": [
    {
      "type": "Feature",
      "id": 1,
      "geometry": null,
      "properties": {
        "F_CODE": "AL030",
        "ZI005_FNA": "مقبرة البحارة"
      }
    },
    {
      "type": "Feature",
      "id": 2,
      "geometry": null,
      "properties": {
        "F_CODE": "AL130",
        "ZI005_FNA": "ساحة الكرامة"
      }
    },
    {
      "type": "Feature",
      "id": 3,
      "geometry": null,
      "properties": {
        "F_CODE": "BH075",
        "ZI005_FNA": "نافورة البانوراما"
      }
    },
    {
      "type": "Feature",
      "id": 4,
      "geometry": null,
      "properties": {
        "F_CODE": "AK121",
        "ZI005_FNA": "مدرج درعا الأثري"
      }
    },
    {
      "type": "Feature",
      "id": 5,
      "geometry": null,
      "properties": {
        "F_CODE": "AL012",
        "ZI005_FNA": "Roman Graves"
      }
    }
  ]
}
```
