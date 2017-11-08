# Implementations

## Overview

This page points to servers implementing WFS 3.0 drafts.
For now this is limited to implementations of the current
draft of part 1.

Implementations:
* [interactive instruments](#interactive-instruments)
* ...

## interactive instruments

The following are two servers implementing most of the current draft
of part 1. They are using German data and therefore the language
in general is German, including in the HTML.

The first endpoint is for cadastral parcels, buildings and
administrative areas in North-Rhine Westphalia (Germany).
The second endpoint for topographic data in that region.

OpenAPI documents:
* https://www.ldproxy.nrw.de/kataster/api/
* https://www.ldproxy.nrw.de/topographie/api/

HTML landing pages:
* https://www.ldproxy.nrw.de/kataster/
* https://www.ldproxy.nrw.de/topographie/

Since the code generation tools do not yet support OpenAPI 3.0 well, we
have created OpenAPI/Swagger 2.0 definitions for the APIs and published
them on Swagger Hub, too:
* https://app.swaggerhub.com/apis/cportele/lika-nrw/0.0.1
* https://app.swaggerhub.com/apis/cportele/topo-nrw/0.0.1

The implementations are proxy services that sit on top of WFS 2.0 instances.
