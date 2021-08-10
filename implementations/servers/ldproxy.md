# ldproxy

The following APIs are available as an [OGC Reference Implementation](https://www.opengeospatial.org/resource/products/details/?pid=1598). The APIs support Features part 1, 2 and 3. They also implement drafts of OGC API Tiles and Styles.

* Daraa dataset (used in several OGC testbeds and pilots):
  * OpenAPI definition: https://demo.ldproxy.net/daraa/api
  * Landing page: https://demo.ldproxy.net/daraa
* Vineyards in Rhineland-Palatinate dataset:
  * OpenAPI definition: https://demo.ldproxy.net/vineyards/api
  * Landing page: https://demo.ldproxy.net/vineyards

Most resources are available as HTML and JSON. Add `f=json` or `f=html` to override HTTP content negotiation.

Sample requests:

* A conformance declaration: https://demo.ldproxy.net/vineyards/conformance
* Available collections: https://demo.ldproxy.net/daraa/collections
* A collection in a dataset (agricultural surfaces): https://demo.ldproxy.net/daraa/collections/AgricultureSrf
* First page of features in a collection (ground transportation points): https://demo.ldproxy.net/daraa/collections/TransportationGroundPnt/items
* The same features in Web Mercator: https://demo.ldproxy.net/daraa/collections/TransportationGroundPnt/items?f=json&crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F3857
* A single feature (a cemetery): https://demo.ldproxy.net/daraa/collections/CulturePnt/items/1
* Queryable attributes of a collection (ground transportation curves): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/queryables
* JSON Schema of the features of a collection (ground transportation curves): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/schema
* Features in a spatial area (vineyards between 7.0° and 7.1° East and between 49.9° and 50.0° North): https://demo.ldproxy.net/vineyards/collections/vineyards/items?bbox=7.0%2C49.9%2C7.1%2C50.0
* Features selected by an attribute value (vineyards in Lieser): https://demo.ldproxy.net/vineyards/collections/vineyards/items?village=Lieser
* Same query using a CQL2 filter: https://demo.ldproxy.net/vineyards/collections/vineyards/items?filter=village%3D%27Lieser%27
* Features selected by time (ground transportation curves last updated in 2011/2012): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/items?datetime=2011-01-01/2012-12-31
* Features selected by space, time and attributes (ground transportation curves last updated in 2011/2012, in the city of Daraa, restricted to roads): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/items?F_CODE=AP030&bbox=36.08%2C32.59%2C36.12%2C32.64&datetime=2011-01-01%2F2012-12-31

Various datasets from the German state North-Rhine Westphalia are published at https://ogc-api.nrw.de/.

More information about ldproxy:

* [GitHub repository with source code and documentation](https://github.com/interactive-instruments/ldproxy)
* [Step-by-step description how to set up the Vineyards API](https://github.com/interactive-instruments/ldproxy/tree/master/demo/vineyards)
