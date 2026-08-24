# Test dataset for the Abstract Test Suite

This directory contains the test dataset referenced by the Abstract Test Suite (Annex A)
of OGC API - Features - Part 4 / OGC API - Common - Part 5: Create, Replace, Update and Delete.

To use the executable tests with the test dataset, the Web API under test publishes the
dataset as a feature collection that supports the CREATE, REPLACE, UPDATE and DELETE
operations with GeoJSON (`application/geo+json`) and JSON Merge Patch
(`application/merge-patch+json`) and that publishes the schema of the collection.
For the GML tests, the Web API also supports GML (`application/gml+xml`) as a feature
representation in mutation requests, using the feature type from the GML application
schema `buildings.xsd`.

| File | Description |
| ---- | ----------- |
| `buildings.json` | A GeoJSON feature collection with three building features (`B.1`, `B.2`, `B.3`) that are replaced, updated and deleted during the tests. Each feature has an `updated` property with the timestamp of the last change, from which the server derives the `Last-Modified` header for the Optimistic Locking using Timestamps tests. |
| `buildings-schema.json` | The logical schema of the feature collection (Returnables and Receivables, see OGC API - Features - Part 5: Schemas) with a required property `function`. |
| `create-building.json` | A valid new building feature for CREATE tests. |
| `create-building-invalid.json` | A building feature that does not conform to the schema (the required property `function` is missing), for the tests of the Handling Preference conformance class. |
| `create-building-jsonfg.json` | A valid new building feature with JSON-FG extensions; the geometry is provided in the `place` member in the coordinate reference system EPSG:25832. |
| `replace-building.json` | A replacement representation of the building `B.2`. |
| `buildings.xsd` | The GML application schema of the feature type (GML Simple Features Profile, Level 0), for the GML tests. |
| `create-building.gml` | A valid new building feature in GML; the geometry declares the coordinate reference system EPSG:25832 in the `srsName` attribute (the same feature as `create-building-jsonfg.json`). |
| `replace-building.gml` | A replacement representation of the building `B.2` in GML. |
| `update-building.json` | A JSON Merge Patch document for the building `B.3`: changes the primary geometry, changes `height`, adds `owner`, and removes `name`. |
