This folder contains requirements description.

Each file is a single requirement. The naming convention for these files is:

"cc/REQ_req.adoc" where "cc" corresponds to the identifier for the requirements class and "req" corresponds to the identifier for the requirement. Example: "core/REQ_f-op.adoc".

The requirement files are integrated into the main document as links.

The requirement is expressed according to this pattern:

````
[[req_cc_req]]
[width="90%",cols="2,6a"]
|===
^|*Requirement {counter:req-id}* |*/req/cc/req*
^|A |... SHALL ...
^|B |... SHALL ...
|===
````

Multiple statements should only be in a single requirement, if there is a direct
dependency.

For each requirement, there should be a corresponding Abstract Test in the "abstract_tests" folder.
