# OGC API - Features, an overview

All versions of the WFS standard use a Remote-Procedure-Call-over-HTTP architectural style using XML for any payloads as it was state-of-the-art in the late 1990s and early 2000s, when WFS was originally designed. The current WFS 2.x draft standard made a significant start towards modernization by introducing a REST binding, but was still encumbered by legacy design decisions.

OGC API Features will specify a modernized service that aligns with the current architecture of the Web and the Spatial Data on the Web Best Practices. The key changes are:

*	Architecture: OGC API Features supports and is consistent with HTTP and HTTPS. In addition, the resources provided by the server include hypermedia controls in their representations to guide the user of the API. In WFS, HTTP is mainly used as a tunnel for WFS messages.
*	Encodings: WFS is strongly tied to XML (Capabilities documents, XML schemas, Filter Encoding expressions, GML encoding). OGC API Features has been written with HTML, JSON and XML as encodings in mind, because these are common encodings today, but no encoding is mandatory and other encodings may be used as well. HTTP is designed to support the use of multiple formats and defines rules how servers can return the encoding that the client can handle best (“content negotiation”).
*	Reuse: The use of OGC-specific resources or components is minimized in the OGC API and, where available, existing industry-standards that are commonly used by developers are used instead. The most important example for this is the use of OpenAPI definition instead of OGC-specific "Capabilities" documents.
*	Modularization: The WFS 2.0 standard, together with the Filter Encoding 2.0 standard, specifies a powerful, but complex service interface. In order to better support implementations that only need a relatively simple service or client, the OGC API Features is modularized into multiple parts. The first part (the "core") specifies a simple interface to access spatial data that is sufficient for cases that do not require support for transactions, complex data structures, rich queries, custom coordinate reference systems, etc. Additional parts will specify extensions to this part to meet the needs of use cases that require such capabilities.
*	Schemas: WFS required XML schemas for all feature types and valid XML documents. While the capability to support application schemas will be maintained in OGC API Features, it should no longer be required that rigid schemas are provided and used for validation of feature data.
*	Security: WFS 2.0 does not specify how services may be secured and some requirements are incompatible with secured services that still conform to the standard. The use of OpenAPI would address this issue, too. Web APIs may be secured using security schemes that are commonly used on the Web today (e.g., OAuth2) and that developers are familiar with.

As a result of this modernization, OGC API implementations will not be backwards compatible with WFS 2.0 implementations. However, it is a design goal to define OGC API Features in a way so that the Web API can be mapped to an WFS 2.0 implementation - at least for the capabilities that were already in scope in WFS 2.0.

OGC API Features is intended to be simpler and more modern, but still an evolution from WFS.

The goal is to develop part 1 of OGC API Features, the foundation for the new version, as quickly as possible and work on additional parts after that, driven by community interest.

An important aspect is to ensure that implementing the standard will lead to efficient implementations, happy developers of both server and client components, and satisfied users of such components.

This has several aspects:
*	Before finalizing parts of OGC API Features, it must be verified that these goals are met. I.e., working implementations of all capabilities must be available and tested. Implementation feedback must be taken into account.
*	A consequence of this is that the period between the availability of what is considered a mature draft and the finalization of the specification may be longer than in the past, depending on the availability of evidence about the suitability of the specification based on implementations.
*	Developers, including those that are not active in OGC or ISO/TC 211, should be encouraged as early as possible to implement the draft and provide feedback. An aspect of this is public access to drafts from the beginning.
*	The use of GitHub in the development is intentional as this is the environment that many developers are familiar with and use on a daily basis.
