This folder contains the Abstract Test Suite.

Each file describes a single test. The naming convention for these files is:

"cc/TESTn.adoc" where "cc" corresponds to the identifier for the requirements class and "n" corresponds to the test number. Numbers should have preceeding zeros appropriate for the total number of tests in the conformance class (e.g., the first test could be TEST001 if less than 1000 tests are anticipated).

The test is expressed according to this pattern:

````
===== Test case title

(( additional discussion, if needed ))

====== a) Test Purpose:
(( description ))

====== b) Pre-conditions:
* (( list all preconditions ))

====== c) Test Method:
* (( steps to execute and assertions to test ))

====== d) References:
* <<req_cc_req,Requirement /req/cc/req>>
````

NOTE: for each test, there must be one or more requirements in the "requirements" folder.
