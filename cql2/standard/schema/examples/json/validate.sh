#!/bin/sh

# validation using https://www.npmjs.com/package/ajv-cli

# validate all examples
for f in *.json
do
    ajv validate -s "../../cql2.json" --spec=draft2020 --validateFormats=false --strict=true --errors=no -d $f
done
