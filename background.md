# Background

Version 2.0 of the Web Feature Service (WFS, ISO 19142) and Filter Encoding (FES, ISO 19143) standards has been published by OGC/ISO in 2009/2010 (with a corrigendum 2.0.2 published by OGC in 2014). By now most of the WFS products that are maintained have implemented version 2.0.

OGC has been processing change requests since 2012 to prepare a new minor revision version (version 2.x). The changes can be split into two categories: Additional capabilities in new conformance classes (units of measure, asynchronous responses, etc.) and adding a REST binding.

To synchronize publication in OGC and ISO, the ongoing work became a joint working group of OGC (via the WFS/FES SWG) and ISO/TC 211 (via PT 19142/43) which held its first meeting in May 2017 at the ISO/TC 211 meeting in Stockholm.

In parallel to the work on the revision, OGC and W3C have collaborated in a joint [W3C/OGC Spatial Data on the Web Working Group](https://www.w3.org/2015/spatial/). A key result of that work is the [Spatial Data on the Web Best Practice](https://www.w3.org/TR/sdw-bp/). The document builds on the general [W3C Data on the Web Best Practice](https://www.w3.org/TR/dwbp/) and adds practices and recommendations that are specific to spatial data. The abstract of the document is:

>"This document advises on best practices related to the publication of spatial data on the Web; the use of Web technologies as they may be applied to location. The best practices presented here are intended for practitioners, including Web developers and geospatial experts, and are compiled based on evidence of real-world application. These best practices suggest a significant change of emphasis from traditional Spatial Data Infrastructures by adopting an approach based on general Web standards. As location is often the common factor across multiple datasets, spatial data is an especially useful addition to the Web of data.”

The Spatial Data on the Web Best Practice is an OGC Best Practice since July 2017. It will be maintained and updated as necessary by the new [Spatial Data on the Web Interest Group](https://www.w3.org/2017/sdwig/) that has started its work in October 2017.

The OGC is discussing how to take the best practices and related developments like the release of the [OpenAPI 3.0 specification](https://www.openapis.org/blog/2017/07/26/the-oai-announces-the-openapi-specification-3-0-0) in July 2017 into account in the evolution of the OGC standards baseline. WFS was the first standard where this has resulted in concrete steps.

A [change proposal](http://ogc.standardstracker.org/show_request.cgi?id=488) to support the best practices was discussed and the joint OGC/ISO working group decided with unanimous consent to accept it as the basis for the development of the next version of WFS, which will be a major revision, i.e. WFS 3.0. The group also decided to open the GitHub repository that is used to develop the specification to the public.

With similar developments to modernize other OGC web service standards, the OGC decided to publish the new Web API standards as new standards under the brand "OGC API".

OGC API standards define modular API building blocks to spatially enable Web APIs in a consistent way. The OpenAPI specification is used to define the API building blocks.

The OGC API family of standards is organized by resource type. What was formerly known as "WFS 3.0 - Part 1: Core" is now "OGC API - Features - Part 1: Core" (version 1.0).

See [here](overview.md) for an overview of the differences between "OGC API - Features - Part 1: Core" and the WFS standard.
