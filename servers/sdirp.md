# SDI Rhineland-Palatinate

The SDIs of the three German Federal States Rhineland-Palatinate, Hesse and Saarland use the mapbender2 ows registry as backend for their geoportal solutions. In the SDIs there are many OpenData classified WFS 2.0 resources registered. It was straightforward to develop a proxy solution, that implements an OGC API - Features interface at one central location.

Most of the core functions are implemented. The WFSs behind the proxy are either based on mapserver or geoserver. The proxy does also create service metadata in form of iso19139 records. One extension is the usage of json-schema to define human readable attribute titles and descriptions at WFS level. The next extension will be the usage of json-ld to give semantical information for the attributes and allow the dynamical creation of rdf-a and other formats.

The code of the current production solution is available on the [OSGEO GIT](https://git.osgeo.org/gitea/armin11/GeoPortal.rlp)
and [OSGEO SVN](https://trac.osgeo.org/mapbender/browser/trunk/mapbender/).

List of available APIs:

* List of all registered OpenData WFSs: https://www.geoportal.rlp.de/mapbender/php/mod_linkedDataProxy.php (some of them wont work, because the database tables don't have primary keys exposed and therefor paging is not possible).

Example requests:

* Transport network (classified roads)
  * Start page: https://www.geoportal.rlp.de/spatial-objects/513
  * API definition (only available in json): https://www.geoportal.rlp.de/spatial-objects/513/api
  * HTML representation for the collection of highway objects: https://www.geoportal.rlp.de/spatial-objects/513/collections/ms:Autobahnen/items?&f=html
  * HTML represenation of single highway 'A3': https://www.geoportal.rlp.de/spatial-objects/513/collections/ms:Autobahnen/items/Autobahnen.A3?f=html

* UNESCO world heritage of the city of Trier (point objects)
  * Start page: https://www.geoportal.rlp.de/spatial-objects/486
  * API definition (only available in json): https://www.geoportal.rlp.de/spatial-objects/486/api
  * HTML representation objects: https://www.geoportal.rlp.de/spatial-objects/486/collections/ms:unesco_welterbe/items?&f=html
  * HTML representation of the description of the amphitheater: https://www.geoportal.rlp.de/spatial-objects/486/collections/ms:unesco_welterbe/items/unesco_welterbe.3730?f=html
