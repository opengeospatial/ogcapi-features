# OGC Common Query Language

This folder contains the content for the OGC API - Features - Part n: CQL extension.

The file, cql.bnf, contains the BNF for a simple query language for OAPIF that
is roughly equivalent in capability to OGC filter.  It is based on the CQL
syntax defined in "OGC® Catalogue Services 3.0 - General Model" (OGC 12-168r6).

This query language can be used as a query parameter in an OAPIF URI.
For example:

   http://.../collection/MyCollection/items?filter="..."&filter-lang=CQL&...

NOTE: The idea here is that two URL query parameters are defined; one whose
      value is the CQL expression (i.e. "filter" in this example) and another
      (i.e. "filter-lang") to indicate that the query language in use 
      (i.e. CQL in this example).
      This allows for other filter language expressions to be supported as well.

The BNF seems to validate using the following BNF parsers:

* https://www.icosaedro.it/bnf_chk/bnf_chk-on-line.html
* https://www.nongnu.org/bnf/

The file, cql.json, is a JSON Schema file that defines a JSON encoding for CQL.
The JSON schema seems to validate using the following validator:

https://json-schema-validator.herokuapp.com/index.jsp

The file, examples.txt, contains example of both CQL and CQL-JSON.

NOTES:

The file 'resources/catCql.bnf' contains the BNF text exactly as it exists
in the OGC Catalogue specification (http://docs.opengeospatial.org/is/12-168r6/12-168r6.html#54).
It is included here for convenience but is, as I have mentioned, pretty rough!

This is a very rough first draft put up here so that more eyes can take a look
at it.  Some outstanding issues include:

* add more comments
* need to add BNF for regular expressions for the LIKE operator
* need to add (or at least consider adding) CIRCLES/ELLIPSE/ARC
* need to add (or at least consider adding) geometry CRS (to go along with CRS extension)
* compare the spatial and temporal predicate sytax to SQLMM
* consider property existence operators; since OAPIF is schema-less it might
  be nice to be able to have predicates like "<propertyName> EXISTS AND 
  <propertyName> = 'some string'".
* CQL support function invocation but how do we advertise which functions
  an implementation supports (... in the OpenAPI document I suppose)
* lexical space for propertyName; right now I just use a very simple production
  for property names but it needs to be extended to handle international
  characters too 
* internationalization for string literals (related to last point)
* right now the CQL handle timezones which means that clients will need
  to handle time zone conversion; do we really want that?
* is there an "official" BNF for the WKT representation of geometry?  If 
  so, we should reference that instead
