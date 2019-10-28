# OGC Common Query Language

This folder contains the content for the OGC API - Features - Part n: CQL extension.

The file, cql.bnf, contains the BNF for a simple query language for OAPIF that
is roughly equivalent in capability to OGC filter.  This query language can
be used as a query parameter in an OAPIF URI.  For example:

http://www.someserver.com/wfs/collection/MyCollection/items?cql="..."&...

This BNF is roughly equivalent to the BNF in the OGC catalogue (which is a
complete mess) but does differ in some aspects.  For example the catalogue
BNF uses functions to implement the spatial operators (e.g.
"OVERLAPS(propertyName,geometry)" ) while this BNF uses a more SQL-like syntax
(e.g. "propertyName OVERLAPS geometry").

The BNF seems to validate using the following BNF parsers:

* https://www.icosaedro.it/bnf_chk/bnf_chk-on-line.html
* https://www.nongnu.org/bnf/

NOTES:

This is a very rough first draft put up here so that more eyes can take a look
at it.  Some outstanding issues include:

* add more comments
* need to add BNF for a URI 
* need to add BNF for regular expressions for the LIKE operator
* need to add (or at least consider adding) CIRCLES/ELLIPSE/ARC
* compare the spatial and temporal predicate sytax to SQLMM
* consider property existence operators; since OAPIF is schema-less it might
  be nice to be able to have predicates like "<propertyName> EXISTS AND 
  <propertyName> = 'some string'".
