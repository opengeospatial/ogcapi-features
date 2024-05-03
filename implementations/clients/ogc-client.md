# ogc-client

[ogc-client](https://github.com/camptocamp/ogc-client) is a Typescript library that offers useful APIs on top of various OGC protocols, including OGC API.

Supported protocols are:

* WMS - Web Map Service
* WFS - Web Feature Service
* WMTS - Web Map Tile Service
* OGC API (Records and Features)

## How to use it

The `OgcApiEndpoint` class lets us interact with an OGC API compliant endpoint in various ways. Since most operations in an OGC API endpoint revolves around doing requests to various linked addresses,
this class offers an abstraction pased on simple promises.

For instance, to get a list of collections:

```js
const endpoint = new OgcApiEndpoint('https://my.endpoint.org/ogcapi');
console.log(await endpoint.allCollections);
```

More detailed information on collection can be fetched like so:

```js
const collection = await endpoint.getCollectionInfo('city-roads');
console.log(collection.itemCount);
```

To read items in a collection, the `/items` endpoint can be exploited like so:

```js
const itemsUrl = await endpoint.getCollectionItemsUrl(
  'city-roads',
  {
    asJson: true,
    limit: 10,
    offset: 30
  }
);
fetch(itemsUrl).then(resp => resp.json()).then(...)
```

Items can also be fetched in bulk, often using more diverse formats:

```js
const flatgeobufUrl = collection.bulkDownloadLinks['application/flatgeobuf'];
fetch(flatgeobufUrl).then(resp => resp.arrayBuffer()).then(...)
```

See https://camptocamp.github.io/ogc-client/#/api for more details on the API of ogc-client.
