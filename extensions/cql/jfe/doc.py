import json
from string import Template
from jsonschema import Draft7Validator

group_template = Template(
    """
### ${title}
"""
)

expression_template = Template(
    """
#### `${title}`

${description}

```json
${example}
```
"""
)

base = "#/definitions/"


def get_def(schema, ref):
    definitions = schema["definitions"]
    id = ref[len(base) :]
    return definitions[id], id


def get_doclet(validator, expression):
    for example in expression["examples"]:
        validator.validate(example)

    all_examples = "\n```\n\n```json\n".join(
        [json.dumps(example) for example in expression["examples"]]
    )

    return expression_template.substitute(
        title=expression["title"],
        description=expression["description"],
        example=all_examples,
    )


def get_docs():
    with open("schema.json", "r") as f:
        schema = json.load(f)

    validator = Draft7Validator(schema)

    docs = ""
    root, _ = get_def(schema, schema["$ref"])

    visited = ()
    for entry in root["oneOf"]:
        ref = entry.get("$ref")
        if not ref or "title" not in entry:
            continue

        docs += group_template.substitute(**entry)

        group, _ = get_def(schema, ref)
        for entry in group["oneOf"]:
            ref = entry.get("$ref")
            if not ref:
                continue

            expression, id = get_def(schema, ref)
            if "title" in expression:
                docs += get_doclet(validator, expression)
                visited += (id,)

    docs += group_template.substitute(title="Utility Expressions")
    definitions = schema["definitions"]
    for id, entry in definitions.items():
        if id in visited or "title" not in entry:
            continue

        docs += get_doclet(validator, entry)

    return docs


if __name__ == "__main__":
    print(get_docs())

