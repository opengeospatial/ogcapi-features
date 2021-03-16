# nls-fi

Topographical database of National Land Survey of Finland as an OGC API - Features with some 130 collections. Powered by a server called hakuna-wfs3, implemented in Java at the NLS-Finland. Currently supporting JSON/GeoJSON (and also MVT for /tiles). Pagination via primary keys, fully streaming approach.

Example requests:

* OpenAPI document: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/api
* First 10 roadlinks: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/collections/tieviiva/items?limit=10
* Roadlink with id 11: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/collections/tieviiva/items/11
* First 1000 buildings inside 380000,6670000,390000,6680000,EPSG:3067: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/collections/rakennus/items?bbox=380000,6670000,390000,6680000&bbox-crs=http://www.opengis.net/def/crs/EPSG/0/3067&crs=http://www.opengis.net/def/crs/EPSG/0/3067&limit=1000
