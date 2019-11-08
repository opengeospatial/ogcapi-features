# JSON Filter Expressions

This directory includes resources describing a JSON encoding for filter expressions.  The intention of these resources is to describe a language to be used in a filter extension for the OGC API – Features spec.

## Examples

As an example, given a collection of features representing buildings, the filter expression below would match all items that have a height property that is greater than 50:

```json
[">" ["get", "height"], 50]
```

See the [examples.md](./examples.md) file for more examples.

## Language

JSON filter expressions are a subset of JSON with a grammar that follows these [rules](https://en.wikipedia.org/wiki/Augmented_Backus%E2%80%93Naur_form):

    expression = begin-array operator *( value-separator argument ) end-array

    operator = quotation-mark 1*char quotation-mark

    argument = false / null / true / object / number / string / expression

See the [JSON grammar](https://tools.ietf.org/html/rfc8259) for a definition of the
rules for `begin-array`, `value-separator`, `end-array`, `quotation-mark`, `char`, `false`, `null`,
`true`, `object`, `number`, and `string`.

See the [`schema.json`](./schema.json) file for a JSON Schema doc describing the language.

## Core Operators

The core language defines the operators below.  Implementors could advertise which of these operators they support.  Implementors wishing to add support custom operators could add to the list.

> Note that the block of documentation below is generated from the schema by running `python doc.py`


### Comparison Expressions

#### `==`

Returns true if two values are equal.

```json
["==", ["get", "height"], 42]
```

#### `!=`

Returns true if two values are not equal.

```json
["!=", ["get", "height"], 42]
```

#### `>`

Returns true if the first value is greater than the second.

```json
[">", ["get", "height"], 42]
```

#### `>=`

Returns true if the first value is greater than or equal to the second.

```json
[">=", ["get", "height"], 42]
```

#### `<`

Returns true if the first value is less than the second.

```json
["<", ["get", "height"], 42]
```

#### `<=`

Returns true if the first value is less than or equal to the second.

```json
["<=", ["get", "height"], 42]
```

#### `like`

Returns true if a string is matched by the provided pattern.  The optional third argument can include a wildCard property (defaults to '%').

```json
["like", ["get", "name"], "% Smith"]
```

```json
["like", ["get", "name"], "* Smith", {"wildCard": "*"}]
```

#### `in`

Returns true if the first value is equal to at least one of the following values.

```json
["in", ["get", "class"], "business", "factory", "mercantile"]
```

### Spatial Expressions

#### `intersects`

Returns true if two geometries intersect one another.

```json
["intersects", ["geometry"], {"type": "Point", "coordinates": [0, 0]}]
```

#### `within`

Returns true if the first geometry is completely within the second.

```json
["within", {"type": "Point", "coordinates": [0, 0]}, ["geometry"]]
```

### Temporal Expressions

#### `before`

Returns true if the first time occurs before the second time.  String values are interpreted as RFC-3339 formatted date-times.

```json
["before", ["get", "updated"], "2017-06-10T07:30:00Z"]
```

#### `after`

Returns true if the first time occurs after the second time.  String values are interpreted as RFC-3339 formatted date-times.

```json
["after", ["get", "updated"], "2017-06-10T07:30:00Z"]
```

#### `during`

Returns true if the first time occurs during the interval time given by the start and end date-times (inclusive).  String values are interpreted as RFC-3339 formatted date-times.

```json
["during", ["get", "built"], "2017-06-10T07:30:00Z", "2018-06-10T07:30:00Z"]
```

### Logical Expressions

#### `all`

Returns true if all of the arguments evaluate to true.

```json
["all", [">", ["get", "height"], 50], ["==", ["get", "type"], "commercial"], ["get", "occupied"]]
```

#### `any`

Returns true if any of the arguments evaluate to true.

```json
["any", ["<", ["get", "height"], 50], ["!", ["get", "occupied"]]]
```

#### `!`

Returns the opposite of a boolean value.

```json
["!", ["get", "private"]]
```

### Utility Expressions

#### `get`

Get a property value.

```json
["==", ["get", "height"], 50]
```

#### `id`

Get the feature identifier.

```json
["==", ["id"], "b087dd1d-f2bb-4bf5-ada5-c3d9cd35ef75"]
```

#### `geometry`

Get the feature's geometry.  The optional second arg can be used to get a non-default geometry.

```json
["intersects", ["geometry"], {"type": "Point", "coordinates": [0, 0]}]
```

```json
["intersects", ["geometry", "location"], {"type": "Point", "coordinates": [0, 0]}]
```

#### `bbox`

Returns a polygon geometry from the provided min longitude, min latitude, max longitude, max latitude values.

```json
["intersects", ["geometry"], ["bbox", -180, -90, 180, 90]]
```

#### `+`

Returns the sum of two or more values.

```json
[">", ["+", ["get", "age"], ["get", "income"]], 100]
```

#### `-`

Returns the result of subtracting the second value from the first.

```json
[">", ["-", ["get", "age"], ["get", "income"]], 10]
```

#### `*`

Returns the product of two or more values.

```json
[">", ["*", ["get", "age"], ["get", "income"]], 1000]
```

#### `/`

Returns the result of dividing the first value by the first.

```json
[">", ["/", ["get", "width"], ["get", "height"]], 1.5]
```

#### `%`

Returns the remainder after integer division of the first value by the second.

```json
[">", ["%", ["get", "width"], 256], 128]
```

#### `floor`

Returns the largest integer less than or equal to a given number.

```json
["==", ["floor", ["get", "age"]], 42]
```

#### `ceil`

Returns the smallest integer greater than or equal to a given number.

```json
["==", ["ceil", ["get", "age"]], 42]
```

#### `abs`

Returns the absolute value of a number.

```json
[">", ["abs", ["get", "delta"]], 1]
```

#### `^`

Returns the result of raising the first value to the power given by the second.

```json
[">", ["^", ["get", "size"], 2], 100]
```

#### `min`

Returns smallest of two or more values.

```json
[">", ["min", ["get", "wins"], ["get", "ties"]], 10]
```

#### `max`

Returns largest of two or more values.

```json
[">", ["max", ["get", "wins"], ["get", "ties"]], 10]
```


## Tests

The [`fixtures`](./fixtures) directory includes valid and invalid test fixtures.  To validate the schema and assert that these fixtures are invalid or valid, run the tests (this assumes you have run `pip install -r requirements.txt` to get the test dependencies):

```
python test.py
```

## Implementations

 * National Land Survey of Finland OGC API – Features implementation at https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/features/v1/ with experimental support for `filter-lang=json-filter-expr`.  E.g. `https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/features/v1/collections/tieviiva/items?limit=100&filter-lang=json-filter-expr&filter=["==",["get","kohdeluokka"],12316]`

 * Experimental support in GDAL (using `filter-lang=json-filter-expr`) - https://github.com/OSGeo/gdal/pull/1999

 * Generic Golang parser for JSON (Filter) Expressions - https://godoc.org/github.com/tschaub/jiffy

 * Support for JSON Filter Expression parsing in pygeofilter - https://github.com/geopython/pygeofilter

## Prior Art

 * [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language))
 * [The Mapbox style specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/)
