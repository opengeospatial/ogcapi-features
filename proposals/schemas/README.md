# OGC API - Features - Part n: Schemas

This folder contains an outline for the "Schemas" extension of the OGC API Features standard.

THIS IS CURRENTLY A PROPOSAL DRAFT. It is based on the current drafts of Part 3 and Part 4 as well as Records Part 1.

OGC API Features does not require that features have a documented schema or that features of a collection are restricted to some schema. In many cases, however, there will be a feature schema, for example, if features use a datastore that consists of tables. Or clients require schema information to make use certain API building blocks, for example, they need to know which feature properties can be used in filter expressions or to sort results.

Schemas will be published on the collection level. The standard will define two requirements classes:

- "Schema" will specify the Schema resource at the endpoint `/collections/{collectionId}/schema`. The only method that will be specified is GET (as usual, HEAD and OPTIONS should be supported, too) and the response will depend on the value of a query parameter `type`.
  - `returnables` (default): The schema will specify an object as it is returned at the `/collections/{collectionId}/items/{featureId}` endpoints of the collection.
  - `queryables`: The schema will specify an object and one property for each property that can be used in `filter` expressions. The schema description for each property should provide sufficient information so that clients can construct meaningful queries. Conditional dependency: http://www.opengis.net/spec/ogcapi-features-3/1.0/req/filter.
  - `sortables`: The schema will specify an object and one property for each property that can be used in `sortby` expressions. Conditional dependency: http://www.opengis.net/spec/ogcapi-records-1/1.0/req/sorting.
  - `create`: The schema will specify an object as it is accepted for POST requests to the `/collections/{collectionId}/items` endpoint of the collection. Conditional dependency: http://www.opengis.net/spec/ogcapi-features-4/1.0/req/create-replace-delete.
  - `replace`: The schema will specify an object as it is accepted for PUT requests to the `/collections/{collectionId}/items/{featureId}` endpoints of the collection. Conditional dependency: http://www.opengis.net/spec/ogcapi-features-4/1.0/req/create-replace-delete.
  - `update`: The schema will specify an object as it is accepted for PATCH requests to the `/collections/{collectionId}/items/{featureId}` endpoints of the collection. Conditional dependency: http://www.opengis.net/spec/ogcapi-features-4/1.0/req/update.
- "Schema (Features)" will specify the requirements for implementations that support "Schema" and http://www.opengis.net/spec/ogcapi-features-1/1.0/req/core. The requirements apply only to collections with no `itemType` or with a value "feature".
  - Conditional dependency: http://www.opengis.net/spec/ogcapi-features-1/1.0/req/geojson
    - Dependency: JSON Schema 2020-12 and 2019-09
    - The JSON Schema version will be selected with a query parameter `profile`.
    - The endpoint will support a JSON Schema response for the `returnables` schema describing the schema of the GeoJSON feature.
    - Conditional dependency: http://www.opengis.net/spec/ogcapi-features-3/1.0/req/filter. The endpoint will support a JSON Schema response for the `queryables` schema.
    - Conditional dependency: http://www.opengis.net/spec/ogcapi-records-1/1.0/req/sorting. The endpoint will support a JSON Schema response for the `sortables` schema.
    - Conditional dependency: http://www.opengis.net/spec/ogcapi-features-4/1.0/req/create-replace-delete. The endpoint will support a JSON Schema response for the `create` schema describing the schema of the GeoJSON feature. This schema will in general be the based as the `returnables` schema, but some common reasons for differences: `id` and `links` is not part of the schema as these will be managed by the server; additional properties beyond those explicitly listed are prohibited.
    - Conditional dependency: http://www.opengis.net/spec/ogcapi-features-4/1.0/req/create-replace-delete. The endpoint will support a JSON Schema response for the `replace` schema describing the schema of the GeoJSON feature. This schema will in general be similar to the `create` schema, but can differ in how `id` is handled.
    - Conditional dependency: http://www.opengis.net/spec/ogcapi-features-4/1.0/req/update. The endpoint will support a JSON Schema response for the `update` schema describing the schema of the GeoJSON feature. This schema will remove any `required` statements and allow `null` for properties that are not mandatory to support JSON Merge Patch.
  - If there are three implementation commitments we could also add support for GML and XML Schema.

Part 3, Part 4 and Records Part 1 will be updated to remove their schema discussions and reference this part.

## Examples

The examples do not include the `$schema` and `$id` members. They are identical for drafts 2020-12 and 2019-09.

### Returnables

```json
{
  "type": "object",
  "title": "Cultural (Points)",
  "description": "Cultural: Information about features on the landscape that have been constructed by man.",
  "required": [
    "type",
    "geometry",
    "properties"
  ],
  "properties": {
    "type": {
      "type": "string",
      "enum": [
        "Feature"
      ]
    },
    "id": {
      "type": "integer"
    },
    "links": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/Link"
      }
    },
    "geometry": {
      "oneOf": [
        {
          "type": "null"
        },
        {
          "type": "object",
          "title": "GeoJSON Point",
          "required": [
            "type",
            "coordinates"
          ],
          "properties": {
            "type": {
              "type": "string",
              "enum": [
                "Point"
              ]
            },
            "coordinates": {
              "type": "array",
              "items": {
                "type": "number"
              },
              "minItems": 2,
              "maxItems": 3
            }
          }
        }
      ]
    },
    "properties": {
      "type": "object",
      "properties": {
        "FCSUBTYPE": {
          "type": "integer",
          "title": "Feature Subtype Code"
        },
        "F_CODE": {
          "type": "string",
          "title": "Feature Type",
          "enum": [
            "AK121",
            "AL012",
            "AL030",
            "AL130",
            "BH075"
          ]
        },
        "UFI": {
          "type": "string",
          "title": "Unique Entity Identifier"
        },
        "ZI001_SDP": {
          "type": "string",
          "title": "Source Description"
        },
        "ZI001_SDV": {
          "type": "string",
          "title": "Last Change",
          "format": "date-time,date"
        },
        "ZI005_FNA": {
          "type": "string",
          "title": "Name"
        },
        "ZI006_MEM": {
          "type": "string",
          "title": "Memorandum"
        },
        "ZI037_REL": {
          "type": "integer",
          "title": "Religious Designation",
          "enum": [
            -999999,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14
          ]
        }
      }
    }
  },
  "$defs": {
    "Link": {
      "type": "object",
      "required": [
        "href"
      ],
      "properties": {
        "href": {
          "type": "string",
          "format": "uri-reference"
        },
        "rel": {
          "type": "string"
        },
        "type": {
          "type": "string"
        },
        "title": {
          "type": "string"
        }
      }
    }
  }
}
```

### Queryables

```json
{
  "type" : "object",
  "title" : "Cultural (Points)",
  "description" : "Cultural: Information about features on the landscape with a point geometry that have been constructed by man.",
  "properties" : {
    "F_CODE" : {
      "title" : "Feature Type",
      "type" : "string",
      "enum" : [ "AK121", "AL012", "AL030", "AL130", "BH075" ]
    },
    "ZI001_SDV" : {
      "title" : "Last Change",
      "type" : "string",
      "format" : "date-time"
    },
    "ZI037_REL" : {
      "title" : "Religious Designation",
      "type" : "integer",
      "enum" : [ -999999, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 ]
    },
    "geometry" : {
      "$ref" : "https://geojson.org/schema/Point.json"
    }
  }
}
```

### Sortables

```
{
  "type" : "object",
  "title" : "Cultural (Points)",
  "description" : "Cultural: Information about features on the landscape with a point geometry that have been constructed by man.",
  "properties" : {
    "F_CODE" : {
      "title" : "Feature Type",
      "type" : "string"
    },
    "ZI001_SDV" : {
      "title" : "Last Change",
      "type" : "string",
      "format" : "date-time"
    },
    "ZI037_REL" : {
      "title" : "Religious Designation",
      "type" : "integer"
    }
  }
}
```

### Create

```json
{
  "type": "object",
  "title" : "Buildings",
  "description" : "...",
  "required": [
     "type",
     "geometry",
     "properties"
  ],
  "additionalProperties": false,
  "properties": {
     "id": {
        "type": [ "string", "integer" ]
     },
     "type": {
        "type": "string",
        "enum": [ "Feature" ]
     },
     "geometry": {
        "$ref": "https://geojson.org/schema/Polygon.json"
     },
     "properties": {
        "type": "object",
        "required": [
           "apnid",
           "bldgid2",
           "bldgtype",
           "final_apn"
        ],
        "properties": {
           "shape_len": {
              "type": "number",
              "format": "double"
           },
           "shape_area": {
              "type": "number",
              "format": "double"
           },
           "bldgid3": {
              "type": "string"
           },
           "bldgid2": {
              "type": "string"
           },
           "bldgtype": {
              "type": "string",
              "enum": ["Commercial Building", ...]
           },
           "final_apn": {
              "type": "string",
              "pattern": "\\d{13}"
           },
           "apnid": {
              "type": "number",
              "format": "integer"
           },
           "nostory": {
              "type": "number",
              "format": "integer",
              "minimum": 1,
              "maximum": 400
           },
           "bldgnum": {
              "type": "string"
           },
           "numbldgs": {
              "type": "number",
              "format": "integer"
           },
           "comname": {
              "type": "string"
           }
        }
     }
  }
}
```

### Replace

```json
{
  "type": "object",
  "title" : "Buildings",
  "description" : "...",
  "required": [
     "type",
     "geometry",
     "properties"
  ],
  "additionalProperties": false,
  "properties": {
     "id": {
        "type": [ "string", "integer" ]
     },
     "type": {
        "type": "string",
        "enum": [ "Feature" ]
     },
     "geometry": {
        "$ref": "https://geojson.org/schema/Polygon.json"
     },
     "properties": {
        "type": "object",
        "required": [
           "apnid",
           "bldgid2",
           "bldgtype",
           "final_apn"
        ],
        "properties": {
           "shape_len": {
              "type": "number",
              "format": "double"
           },
           "shape_area": {
              "type": "number",
              "format": "double"
           },
           "bldgid3": {
              "type": "string"
           },
           "bldgid2": {
              "type": "string"
           },
           "bldgtype": {
              "type": "string",
              "enum": ["Commercial Building", ...]
           },
           "final_apn": {
              "type": "string",
              "pattern": "\\d{13}"
           },
           "apnid": {
              "type": "number",
              "format": "integer"
           },
           "nostory": {
              "type": "number",
              "format": "integer",
              "minimum": 1,
              "maximum": 400
           },
           "bldgnum": {
              "type": "string"
           },
           "numbldgs": {
              "type": "number",
              "format": "integer"
           },
           "comname": {
              "type": "string"
           }
        }
     }
  }
}
```

### Update

```json
{
  "type": "object",
  "title" : "Buildings",
  "description" : "...",
  "additionalProperties": false,
  "properties": {
     "type": {
        "type": "string",
        "enum": [ "Feature" ]
     },
     "geometry": {
        "$ref": "https://geojson.org/schema/Polygon.json"
     },
     "properties": {
        "type": "object",
        "properties": {
           "shape_len": {
              "oneOf": [
                 { "type": "number", "format": "double" },
                 { "type": "null" }
              ]
           },
           "shape_area": {
              "oneOf": [
                 { "type": "number", "format": "double" },
                 { "type": "null" }
              ]
           },
           "bldgid3": {
              "type": [ "string", "null" ]
           },
           "bldgid2": {
              "type": "string"
           },
           "bldgtype": {
              "type": "string",
              "enum": ["Commercial Building", ...]
           },
           "final_apn": {
              "type": "string",
              "pattern": "\\d{13}"
           },
           "apnid": {
              "type": "number",
              "format": "integer"
           },
           "nostory": {
              "oneOf": [
                 {
                    "type": "number",                        
                    "format": "integer",
                    "minimum": 1,
                    "maximum": 400
                 },
                 { "type": "null" }
              ]
           },
           "bldgnum": {
              "type": [ "string", "null" ]
           },
           "numbldgs": {
              "oneOf": [
                 { "type": "number", "format": "integer" },
                 { "type": "null" }
              ]
           },
           "comname": {
              "type": [ "string", "null" ]
           }
        }
     }
  }
}
```
