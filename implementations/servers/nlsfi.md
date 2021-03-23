# nls-fi

Topographical database of National Land Survey of Finland as an OGC API - Features with some 130 collections. Powered by a server called hakuna-wfs3, implemented in Java at the NLS-Finland. Currently supporting JSON/GeoJSON (and also MVT for /tiles). Pagination via primary keys, fully streaming approach.

The service requires an API key! You can create one by self registering at https://omatili.maanmittauslaitos.fi/?lang=en (requires valid email address). Use the API key as the username in HTTP Basic Auth (password is ignored) or as query parameter ('api-key') as in the examples below.

Example requests:

* OpenAPI document
* https://avoin-paikkatieto.maanmittauslaitos.fi/maastotiedot/features/v1/api?api-key=<API_KEY>
* First 10 roadlinks
* https://avoin-paikkatieto.maanmittauslaitos.fi/maastotiedot/features/v1/collections/tieviiva/items?limit=10&api-key=<API_KEY>
* Roadlink with id 11
* https://avoin-paikkatieto.maanmittauslaitos.fi/maastotiedot/features/v1/collections/tieviiva/items/11?api-key=<API_KEY>
* First 1000 buildings inside 380000,6670000,390000,6680000,EPSG:3067
* https://avoin-paikkatieto.maanmittauslaitos.fi/maastotiedot/features/v1/collections/rakennus/items?bbox=380000,6670000,390000,6680000&bbox-crs=http://www.opengis.net/def/crs/EPSG/0/3067&crs=http://www.opengis.net/def/crs/EPSG/0/3067&limit=1000&api-key=<API_KEY>
