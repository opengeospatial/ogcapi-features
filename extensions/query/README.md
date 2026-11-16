# OGC API - Features - Part 10: Query

This folder contains the text for part 10 of the OGC API Features suite of standards.

This document is a draft. It is not an OGC Standard.

This document specifies an extension that defines the behaviour of a server
that supports searching for resources from one or more collections.  This
part supports queries that cannot be expressed, or cannot be conveniently
expressed, using the filtering mechanisms available in Parts 1 or 3.

Examples of the types of queries that can be expressed using Part 10 are:

* queries with a long expression text that cannot be conveniently specified as URL parameters
* bundled queries that, in a single request, fetch resources from one or more collections
* queries that include predicates that join two or more collections
* stored queries
* stored queries possibly referencing multiple resource collections
* stored queries with parameters

Specifically, this document defines:

* an endpoint, `/query` that can be used to execute ad-hoc queries on multiple collections or discover the available stored queries,
* an endpoint, `/query/{queryId}` that can be used to execute, create, modify or delete stored queries,
* support for parameterized stored queries.

The following table crosswalks each of the resource endpoints discussed in this standard with the HTTP methods GET, POST, PUT and DELETE.  Each intersecting cell in the table either contains a reference to the section in this standard where that combination from resource and method is discussed or the phrase `NOT DEFINED` which is used to indicate that this specification does not describe any behaviour for that combination of resource endpoint and HTTP method.

|Resource endpoint |HTTP METHOD |Description |
|------------------|------------|------------|
|/query |GET    |Get the list of stored queries. |
| |POST   |Execute an ad-hoc search that references multiple collections. |
|/query/{queryId} |GET    |Execute this stored query. |
| |POST   |Execute this stored query with an application/x-www-form-urlencoded body. |
| |PUT    |Create or replace a stored query. |
| |DELETE |Delete this stored query. |
|/query/{queryId}/definition |GET |Get definitions of this stored query. |
|/query/{queryId}/parameters |GET |Get the list of parameters for this parameterized stored query. |
|/query/{queryId}/parameters/{parameterId} |GET |Get the definition of this query parameter. |

The query expressions are encoded in JSON (media type `application/ogc-query+json`) and filters use [CQL2](https://docs.ogc.org/is/21-065r2/21-065r2.html) in its JSON encoding. The examples are simplified; see the draft for the details.

An example of a query on a single collection:

````
   CLIENT                                                               SERVER
     |                                                                     |
     |   POST /query   HTTP/1.1                                            |
     |   Host: www.someserver.com/                                         |
     |   Accept: application/geo+json                                      |
     |   Content-Type: application/ogc-query+json                          |
     |                                                                     |
     |   {                                                                 |
     |      "collections": ["radarsat2"],                                  |
     |      "limit": 500,                                                  |
     |      "filter": {                                                    |
     |         "op": "and",                                                |
     |         "args": [                                                   |
     |            {                                                        |
     |               "op": "like",                                         |
     |               "args": [{"property": "eo_instruments"}, "OLI%"]      |
     |            },                                                       |
     |            {                                                        |
     |               "op": "s_intersects",                                 |
     |               "args": [                                             |
     |                  {"property": "footprint"},                         |
     |                  {                                                  |
     |                     "type": "Polygon",                              |
     |                     "coordinates": [                                |
     |                        [                                            |
     |                           [-79.5442,43.5845],                       |
     |                           [-79.4893,43.6079],                       |
     |                           [-79.4632,43.5677],                       |
     |                           [-79.3925,43.6129],                       |
     |                           [-79.3238,43.6223],                       |
     |                           [-79.3163,43.6576],                       |
     |                           [-79.1178,43.7945],                       |
     |                           [-79.1542,43.8144],                       |
     |                           [-79.1714,43.8555],                       |
     |                           [-79.6390,43.7509],                       |
     |                           [-79.5442,43.5845]                        |
     |                        ]                                            |
     |                     ]                                               |
     |                  }                                                  |
     |               ]                                                     |
     |            }                                                        |
     |         ]                                                           |
     |      }                                                              |
     |   }                                                                 |
     |-------------------------------------------------------------------->|
     |                                                                     |
     |   Content-Type: application/geo+json                                |
     |   {                                                                 |
     |      "type": "FeatureCollection",                                   |
     |      "features": [                                                  |
     |         {                                                           |
     |            "id": "1010",                                            |
     |            "type": "Feature",                                       |
     |            "geometry": { ... },                                     |
     |            "properties": { ... }                                    |
     |         },                                                          |
     |         .                                                           |
     |         .                                                           |
     |         .                                                           |
     |      ]                                                              |
     |   }                                                                 |
     |<--------------------------------------------------------------------|
````

An example of a query expression with multiple queries:

````
   CLIENT                                                               SERVER
     |                                                                     |
     |   POST /query   HTTP/1.1                                            |
     |   Host: www.someserver.com/                                         |
     |   Accept: application/json                                          |
     |   Content-Type: application/ogc-query+json                          |
     |                                                                     |
     |   {                                                                 |
     |      "queries": [                                                   |
     |         { "collections": ["parks"] },                               |
     |         { "collections": ["lakes"] }                                |
     |      ]                                                              |
     |   }                                                                 |
     |-------------------------------------------------------------------->|
     |                                                                     |
     |   Content-Type: application/json                                    |
     |   {                                                                 |
     |      "type": "Collections",                                         |
     |      "collections": [                                               |
     |         {                                                           |
     |            "type": "FeatureCollection",                             |
     |            "features": [                                            |
     |               { ... park feature ... },                             |
     |               .                                                     |
     |               .                                                     |
     |               .                                                     |
     |            ]                                                        |
     |         },                                                          |
     |         {                                                           |
     |            "type": "FeatureCollection",                             |
     |            "features": [                                            |
     |               { ... lake feature ... },                             |
     |               .                                                     |
     |               .                                                     |
     |               .                                                     |
     |            ]                                                        |
     |         }                                                           |
     |      ]                                                              |
     |   }                                                                 |
     |<--------------------------------------------------------------------|
````

An example of a spatial join query:

````
   CLIENT                                                               SERVER
     |                                                                     |
     |   POST /query   HTTP/1.1                                            |
     |   Host: www.someserver.com/                                         |
     |   Accept: application/json                                          |
     |   Content-Type: application/ogc-query+json                          |
     |                                                                     |
     |   {                                                                 |
     |      "collections": ["parks", "lakes"],                             |
     |      "filter": {                                                    |
     |         "op": "and",                                                |
     |         "args": [                                                   |
     |            { "op": "=",                                             |
     |              "args": [{"property": "parks.name"},                   |
     |                       "Algonquin Park"] },                          |
     |            { "op": "s_contains",                                    |
     |              "args": [{"property": "parks.geometry"},               |
     |                       {"property": "lakes.geometry"}] }             |
     |         ]                                                           |
     |      }                                                              |
     |   }                                                                 |
     |-------------------------------------------------------------------->|
     |                                                                     |
     |   Content-Type: application/json                                    |
     |   {                                                                 |
     |      "type": "TupleCollection",                                     |
     |      "tuples": [                                                    |
     |         [                                                           |
     |            {                                                        |
     |               "id": "park.001",                                     |
     |               "type": "Feature",                                    |
     |               "geometry": { ... },                                  |
     |               "properties": { ... }                                 |
     |            },                                                       |
     |            {                                                        |
     |               "id": "lake.001",                                     |
     |               "type": "Feature",                                    |
     |               "geometry": { ... },                                  |
     |               "properties": { ... }                                 |
     |            }                                                        |
     |         ],                                                          |
     |         [                                                           |
     |            { "$ref": "#/tuples/0/0" },                              |
     |            {                                                        |
     |               "id": "lake.002",                                     |
     |               "type": "Feature",                                    |
     |               "geometry": { ... },                                  |
     |               "properties": { ... }                                 |
     |            }                                                        |
     |         ],                                                          |
     |         .                                                           |
     |         .                                                           |
     |         .                                                           |
     |      ]                                                              |
     |   }                                                                 |
     |<--------------------------------------------------------------------|
````
