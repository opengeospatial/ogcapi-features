# WFS

## Part 1 - Core

* Limited to GML-SF0 schemas
* A geodetic WGS84 as the default CRS (depends on the encoding)
* binding: REST mandatory
* encodings: at least one of HTML, GML-SF0 and GeoJSON
* the equivalent to Basic WFS with the following:
** dependency to FES part 1 only
* all presentation parameters; startIndex must only be supported, if the number of features is limited in a response (to support access to all features)
* only resolve=none

## Part 2 - Transactions

* Transactional
* Locking

== Part 3 - Rich application schemas

- Basic WFS with support for richer application schemas
  - GML-SF2
  - other CRS than geodetic WGS84 may be used as the default CRS
  - support for resolve=local
  - dependency to FES part 2
- Plus geometries not included in Simple Features
- Plus 3D

WFS, part 3

WFS, part 4
- GetProperty
- GetDomain

WFS, part 5
- Manage feature types

WFS, part 6
- Manage stored queries

WFS, part x
- etc.

FES, part 1
- Query
- Minimum Ad-hoc Query, XML encoding
  - Everything currently required by Basic WFS, except: sorting
  - Xpath limited as needed for GML-SF0
  - maybe also limited nesting of operators (?)
- Ad-hoc Query, JSON encoding
  - ???

FES, part 2
- etc.
