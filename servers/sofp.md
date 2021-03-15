# sofp

SOFP is an acronym for Simple Observation Features Project. The server carrying the same name is being developed as a part of a joint venture between Vaisala, Finnish Meteorological Institute and Spatineo. The goal is to test WFS 3.0 and a simple feature encoding for observations and measurements (https://github.com/opengeospatial/omsf-profile).

The server is implemented in TypeScript and runs in NodeJS. The architecture allows plugging in any backend or backends, also written in TypeScript. This makes it possible to integrate into existing infrastructure. The open source server includes only an example backend that serves features from a local GeoJSON file. The core server and the example backend are available on dockerhub: https://hub.docker.com/u/sofp

SOFP focuses also on usability and browseability. Using content-negotiation, the server is easy to browse using a typical browser. The server also produces map previews of data returned by the server when data is retrieved as HTML.

Code is available on GitHub:
* SOFP Core (the server itself): https://github.com/vaisala-oss/sofp-core
* SOFP Library (shared code between backends and the core): https://github.com/vaisala-oss/sofp-lib
* SOFP Example Backend: https://github.com/vaisala-oss/sofp-example-backend
* FMI SmartMet Backend: https://github.com/fmidev/smartmet-sofp-backend

Finnish Meteorological Institute hosts a demo server at http://beta.fmi.fi/data/3/wfs/sofp

Example requests:

* OpenAPI 3 document: http://beta.fmi.fi/data/3/wfs/sofp/api.json
* OpenAPI 3 as HTML: http://beta.fmi.fi/data/3/wfs/sofp/api.html
* All feature collections: http://beta.fmi.fi/data/3/wfs/sofp/collections
* Weather observations: http://beta.fmi.fi/data/3/wfs/sofp/collections/opendata_1h/items?observedPropertyName=Temperature,WindSpeedMS,WindDirection&bbox=24.5,60,25.5,60.5&limit=100
