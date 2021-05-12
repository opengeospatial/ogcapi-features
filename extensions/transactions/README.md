# Transaction Extensions 

# Overview 

This directory contains extensions to [OGC API - Features](https://ogcapi.ogc.org/features/) for handling transactions on features.  Two classes of transactions are specified:

* **OGC API - Features - Part 4: Create, Replace, Update and Delete**

   Defines how to make changes on individual resources that are items in a single collection.

* **OGC API - Features - Part n: Atomic, Batch Transactions**

   Defines how to perform complex transactions with atomic or batch semantics operating on, potentially, multiple resources across multiple collections.

## Part 4 - Create, Replace, Update and Delete

### Draft specification status

* [OGC API - Features - Part 4: Create, Replace, Update and Delete](https://docs.ogc.org/DRAFTS/20-002.html)
  * The draft is fairly complete, but needs more implementations, testing and review to move to the final Public Review.

### Create, Replace, Update and Delete overview

OGC API Features Part 4 defines how to create, replace, update and delete individual features from a collection.  The specification defines the following conformance classes:

* [Create/Replace/Delete](https://docs.ogc.org/DRAFTS/20-002.html#create-replace-delete_clause)

   Specifies how to add new feature instances to a collection, how to replace an existing feature instance with a new instance and how to remove feature instances from a collection.

* [Update](https://docs.ogc.org/DRAFTS/20-002.html#update_clause)

  Specifies how to update parts of a feature instance.

* [Optimistic Locking](https://docs.ogc.org/DRAFTS/20-002.html#optimistic_locking_clause)

  Defines an optimistic locking mechanism to support concurrent updates of resources.

* [Features](https://docs.ogc.org/DRAFTS/20-002.html#features_clause)

   Although the focus of this SWG is on features, Part 4 is -- for the most part --  written generically so that it can apply to any resource type.  The idea is that eventually, most of Part 4 would be absorbed into "OGC API - Common" and only this part, dealing specifically with features, would constitute Part 4.

### Examples

#### Creating a new feature

```
   Client                                                              Server
     |                                                                   |
     | POST /collections/oakland_buildings/items   HTTP/1.1              |
     | Content-Type: application/geo+json                                |
     |                                                                   |
     | {                                                                 |
     |   "type": "Feature",                                              |
     |   "geometry": {                                                   |
     |     "type": "MultiPolygon",                                       |
     |     "coordinates": [                                              |
     |     [[[-122.2694982,37.79045922],[ -122.2693624, 37.79041125],    |
     |      [-122.2693518,37.79042521],[ -122.26899, 37.7902858],        |
     |      [-122.2690027,37.79027181],[ -122.2688602, 37.79021705],     |
     |      [-122.2687222,37.790445],[-122.2688582, 37.79049813],        |
     |      [-122.2689084,37.79041634],[ -122.2689473, 37.79041058],     |
     |      [-122.2691974,37.79051029],[ -122.2692367, 37.7906097],      |
     |      [-122.2692201,37.79064271],[ -122.2693538, 37.79069243],     |
     |      [-122.2694982,37.79045922]]]]                                |
     |   },                                                              |
     |   "properties": {                                                 |
     |     "shape_len": 666.635209546,                                   |
     |     "shape_area": 14016.0452102,                                  |
     |     "bldgid3": "11 EMBARCADERO WEST_bldgG102",                    |
     |     "bldgid2": "11 EMBARCADERO WEST",                             |
     |     "bldgtype": "Commercial Building",                            |
     |     "final_apn": "000O042502000",                                 |
     |     "apnid": 21,                                                  |
     |     "nostory": 2,                                                 |
     |     "bldgnum": "bldgG102",                                        |
     |     "numbldgs": 1,                                                |
     |     "comname": "Portobello Office"                                |
     |   }                                                               |
     | }                                                                 |
     |------------------------------------------------------------------>|
     |                                                                   |
     | HTTP/1.1 201 Created                                              |
     | Location: /collections/oakland_buildings/items/OB.2               |
     |<------------------------------------------------------------------|
```

#### Replacing a feature

```
   Client                                                              Server
     |                                                                   |
     | PUT /collections/oakland_buildings/items/OB.2   HTTP/1.1          |
     | Content-Type: application/geo+json                                |
     |                                                                   |
     | {                                                                 |
     |   "type": "Feature",                                              |
     |   "id": "OB.2",                                                   |
     |   "geometry": {                                                   |
     |     "type": "MultiPolygon",                                       |
     |     "coordinates": [                                              |
     |       [[[-122.2678831,37.80088484],[-122.2679268,37.80090136],    |
     |         [-122.2680801,37.80065184],[-122.2677726,37.8005301 ],    |
     |         [-122.2676158,37.80078035],[-122.2678831,37.80088484]]]   |
     |     ]                                                             |
     |   },                                                              |
     |   "properties": {                                                 |
     |     "shape_len": 402.19805753,                                    |
     |     "shape_area": 10117.0666708,                                  |
     |     "bldgid3": "258 11TH ST_bldg1",                               |
     |     "bldgid2": "258 11TH ST",                                     |
     |     "bldgtype": "Store Building",                                 |
     |     "final_apn": "002 006901000",                                 |
     |     "apnid": 847,                                                 |
     |     "nostory": 1,                                                 |
     |     "bldgnum": "bldg1",                                           |
     |     "numbldgs": 1,                                                |
     |     "comname": "John Sardell & Sons"                              |
     |   }                                                               |
     | }                                                                 |
     |------------------------------------------------------------------>|
     |                                                                   |
     | HTTP/1.1 204 OK                                                   |
     |<------------------------------------------------------------------|
```

#### Deleting a feature

```
   Client                                                              Server
     |                                                                     |
     | DELETE /collections/oakland_buildings/items/OB.2   HTTP/1.1         |
     |-------------------------------------------------------------------->|
     |                                                                     |
     | HTTP/1.1 204 OK                                                     |
     |<--------------------------------------------------------------------|
```

#### Updating part of a feature

```
   Client                                                              Server
     |                                                                     |
     | PATCH /collections/oakland_buildings/items/OB.2   HTTP/1.1          |
     | Content-Type: application/merge-patch+json                          |
     |                                                                     |
     | {                                                                   |
     |    "geometry": {                                                    |
     |       "coordinates": [                                              |
     |         [[[-122.2679,37.8009],[-122.2679,37.8009],                  |
     |           [-122.2681,37.8007],[-122.2678,37.8005],                  |
     |           [-122.2676,37.8008],[-122.2679,37.8009]]]                 |
     |       ]                                                             |
     |    },                                                               |
     |    "properties": {                                                  |
     |       "apnid": 1310,                                                |
     |       "primary_material": "red brick"                               |
     |    }                                                                |
     | }                                                                   |
     |-------------------------------------------------------------------->|
     |                                                                     |
     | HTTP/1.1 200 OK                                                     |
     | Content-Type: application/geo+json                                  |
     |                                                                     |
     | {                                                                   |
     |   "type": "Feature",                                                |
     |   "id": "OB.2",                                                     |
     |   "geometry": {                                                     |
     |     "type": "MultiPolygon",                                         |
     |     "coordinates": [                                                |
     |       [[[-122.2679,37.8009],[-122.2679,37.8009],                    |
     |         [-122.2681,37.8007],[-122.2678,37.8005],                    |
     |         [-122.2676,37.8008],[-122.2679,37.8009]]]                   |
     |     ]                                                               |
     |   },                                                                |
     |   "properties": {                                                   |
     |     "shape_len": 402.19805753,                                      |
     |     "shape_area": 10117.0666708,                                    |
     |     "bldgid3": "258 11TH ST_bldg1",                                 |
     |     "bldgid2": "258 11TH ST",                                       |
     |     "bldgtype": "Store Building",                                   |
     |     "final_apn": "002 006901000",                                   |
     |     "apnid": 1310                                                   |
     |     "nostory": 1,                                                   |
     |     "bldgnum": "bldg1",                                             |
     |     "numbldgs": 1,                                                  |
     |     "comname": "John Sardell & Sons"                                |
     |     "primary_material": "red brick"                                 |
     |   }                                                                 |
     | }                                                                   |
     |<--------------------------------------------------------------------|
```

## Part X - Atomic, Batch Transactions

**T.B.D.**

Work on this part has not begun.

The current thinking is that an endpoint would be defined (e.g. **/transactions**) to which a document describing the changes to make (i.e. inserts, updates, replaces and/or deletes) is POST'ed to be processes.  The changes could be handled atomically (i.e. everything succeeds the entire change request is rolled back) or in batch mode where each change is independent of the other changes in the document.

## Server and client implementations

[Overview of tools implementing OGC API Features](../../implementations/README.adoc)

* [Server implementations - examples, more information and how-to guides](../../implementations/servers/README.md)
* [Client implementations - examples, more information and how-to guides](../../implementations/clients/README.md)

## [Contributing](../../CONTRIBUTING.md)

The contributor understands that any contributions, if accepted by the OGC Membership and ISO/TC 211, shall be incorporated into OGC and ISO/TC 211 OGC API standards documents and that all copyright and intellectual property shall be vested to the OGC.

The Features API Standards Working Group (SWG) is the group at OGC responsible for the stewardship of the standard, but is working to do as much work in public as possible.

* [Features API Standards Working Group Charter](../../CHARTER.adoc)
* [Open issues](https://github.com/opengeospatial/ogcapi-features/issues)
* [Proposing changes](https://github.com/opengeospatial/ogcapi-features/wiki/Propose-a-change-to-a-draft-of-a-specification-document)
* [Copy of License Language](https://raw.githubusercontent.com/opengeospatial/ogcapi-features/master/LICENSE)

Pull Requests from contributors are welcomed. However, please note that by sending a Pull Request or Commit to this GitHub repository, you are agreeing to the terms in the Observer Agreement https://portal.ogc.org/files/?artifact_id=92169
