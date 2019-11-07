
0. beamMode is ScanSAR Narrow AND swathDirection is ascending AND
   polarization is "HH+VV+HV+VH" and intersects geom(Washington DC)

CQL
```
beamMode='ScanSAR Narrow' AND
swathDirection='ascending' AND 
polarization='HH+VV+HV+VH' AND
intersects(geometry,POLYGON((-77.117938 38.936860,-77.040604 39.995648,-76.910536 38.892912,-77.039359 38.791753,-77.047906 38.841462,-77.034183 38.840655,-77.033142 38.857490, -77.117938 38.936860)))
```

CQL JSON
```json
[
  "all",
  ["==", ["get", "beamMode"], "ScanSAR Narrow"],
  ["==", ["get", "swathDirection"], "ascending"],
  ["==", ["get", "polarization"], "HH+VV+HV+VH"],
  ["intersects",
    ["geometry"],
    {
      "type": "Polygon",
      "coordinates": [[
        [-77.117938,38.936860],
        [-77.040604,39.995648],
        [-76.910536,38.892912],
        [-77.039359,38.791753],
        [-77.047906,38.841462],
        [-77.034183,38.840655],
        [-77.033142,38.857490],
        [-77.117938,38.936860]
      ]]
    }
  ]
]
```

1. Floors greater than 5

CQL
```
floors > 5
```

CQL JSON
```json
[
  ">", ["get", "floors"], 5
]
```

2. Taxes less than or equal to 500

CQL
```
taxes <= 500
```

CQL JSON
```json
[
  "<=", ["get", "taxes"], 500
]
```

3. Owner name contains 'Jones'

CQL
```
owner LIKE '% Jones %'
```

CQL JSON
```json
[
  "like", ["get", "owner"], "% Jones %"
]
```

4. Owner name starts with 'Mike'

CQL
```
owner LIKE 'Mike%'
```

CQL JSON
```json
[
  "like", ["get", "owner"], "Mike%", {"wildCard": "%"}
]
```


5. Owner name does not contain 'Mike'

CQL
```
owner NOT LIKE '% Mike %'
```

CQL JSON
```json
[
  "!",
  [
    "like", ["get", "owner"], "% Mike %"
  ]
]
```

6. A swimming pool

CQL
```
swimming_pool=true
```

CQL JSON
```json
[
  "==", ["get", "swimming_pool"], true
]
```

7. More than 5 floors and a swimming pool

CQL
```
floors>5 AND swimming_pool=true
```

CQL JSON
```json
[
  "all",
  [">", ["get", "floor"], 5],
  ["==", ["get", "swimming_pool"], true]
]
```

8. A swimming pool and (more than five floors or material is like brick)

CQL
```
swimming_pool=true AND (floors>5 OR material LIKE '%brick')
```

CQL JSON
```json
[
  "all",
  ["==", ["get", "swimming_pool"], true],
  [
    "any",
    [">", ["get", "floor"], 5],
    ["like", ["get", "material"], "%brick"]
  ]
]
```

9. (More than five floors and material is brick) or swimming pool is true

CQL
```
(floors>5 AND metrial='brick') OR swimming_pool=true
```

CQL JSON
```json
[
  "any",
  [
    "all",
    [">", ["get", "floors"], 5],
    ["==", ["get", "material"], "brick"]
  ],
  ["==", ["get", "swimming_pool"], true]
]
```

10. Not under 5 floors or a swimming pool

CQL
```
NOT (floors<5) OR swimming_pool=true
```

CQL JSON
```json
[
  "any",
  [
    "!",
    ["<", ["get", "floors"], 5]
  ],
  ["==", ["get", "swimming_pool"], true]
]
```

11. Owner name starts with 'mike' or 'Mike' and is less than 4 floors
 
CQL
```
(owner LIKE 'mike%' OR owner like 'Mike%') AND floors<4
```

CQL JSON
```json
[
  "all",
  [
    "any",
    ["like", ["get", "owner"], "mike%"],
    ["like", ["get", "owner"], "Mike%"]
  ],
  ["<", ["get", "floors"], 4]
]
```

12. Built before 2015

CQL
```json
built BEFORE '2015-01-01T00:00:00Z'
```

CQL JSON
```json
[
  "before", ["get", "built"], "2015-01-01T00:00:00Z"
]
```

13. Built after June 10, 2017

CQL
```
built AFTER '2017-06-10T00:00:00Z'
```

CQL JSON
```json
[
  "after", ["get", "built"], "2017-06-10T00:00:00Z"
]
```

14. Updated between 7:30am June 10, 2017 and 10:30am June 11, 2017

CQL
```
updated DURING '2017-06-10T07:30:00' '2017-06-11T10:30:00'
```

CQL JSON
```json
[
  "during", ["get", "updated"], "2017-06-10T07:30:00Z", "2017-06-11T10:30:00Z"
]
```

15. Location in the box between -118,33.8 and -117.9,34 in lat/long (geometry 1)

CQL
```
WITHIN(location,ENVELOPE(-118,33.8,-117.9,34)
```

CQL JSON
```json
[
  "within", ["get", "location"], ["bbox", 33.8, -118, 34, -117.9]
]
```

16. Geometry that intersects with geometry 2 (below)

CQL
```
INTERSECTS(geometry,POLYGON((-10.0 -10.0,10.0 -10.0,10.0 10.0,-10.0 -10.0)))
```

CQL JSON
```json
[
  "intersects",
  ["geometry"],
  {
    "type": "Polygon",
    "coordinates": [[[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, -10.0]]]
  }
]
```

17. More than 5 floors and is within geometry 1 (below)

CQL
```
floors>5 AND WITHIN(geometry,ENVELOPE(33.8,-118,34,-117.9))
```

CQL JSON
```json
[
  "all",
  [">", ["get", "floors"], 5],
  ["within", ["geometry"], ["bbox", 33.8, -118, 34, -117.9]]
]
```
