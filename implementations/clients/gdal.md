# GDAL

This page shows how to connect with GDAL to an API that implements OGC API - Features - Part 1: Core.

## Links

- [GDAL OGC API Features driver documentation](https://gdal.org/drivers/vector/oapif.html)

## Software version

This description uses GDAL 3.2.0.

## Required and supported Conformance classes

The API must support the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core), [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) and [OpenAPI 3.0](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas3) conformance classes.

The CRS conformance class from Part 2 (Coordinate Reference Systems by Reference) is not supported. GDAL, however, can also transform the WGS84 geometries returned from the API to other coordinate reference systems as needed.

## Examples

The examples below use the following URLs of OGC API Landing Page resources:

- `https://demo.ldproxy.net/daraa`
- `https://demo.ldproxy.net/zoomstack`

To see more details on the execution flow, add `--debug on`.

### Basic information about an API

```sh
% ogrinfo OAPIF:https://demo.ldproxy.net/zoomstack

INFO: Open of 'OAPIF:https://demo.ldproxy.net/zoomstack'
      using driver 'OAPIF' successful.
1: airports (title: Airports) (Point)
2: names (title: Names) (Point)
3: rail (title: Rail) (Line String)
4: railway_stations (title: Railway Stations) (Point)
5: roads_local (title: Local Roads) (Line String)
6: roads_national (title: National Roads) (Line String)
7: roads_regional (title: Regional Roads) (Line String)
```

### Basic information about a collection (ground transportation - roads and railways)

The direct URL of the resource is https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv.

This collection has both spatial and temporal extents.

```sh
% ogrinfo -al -so OAPIF:https://demo.ldproxy.net/daraa TransportationGroundCrv

INFO: Open of 'OAPIF:https://demo.ldproxy.net/daraa'
      using driver 'OAPIF' successful.

Layer name: TransportationGroundCrv
Metadata:
  DESCRIPTION=Transportation: Information about the principal means of overland movement of people and goods from one location to another.
  TEMPORAL_INTERVAL_MAX=2015-12-08T20:51:26Z
  TEMPORAL_INTERVAL_MIN=2010-12-30T16:14:46Z
  TITLE=Transportation - Ground (Curves)
Geometry: Multi Line String
Feature Count: 3694
Extent: (35.902874, 32.416814) - (36.574769, 33.142435)
Layer SRS WKT:
GEOGCRS["WGS 84",
    DATUM["World Geodetic System 1984",
        ELLIPSOID["WGS 84",6378137,298.257223563,
            LENGTHUNIT["metre",1]]],
    PRIMEM["Greenwich",0,
        ANGLEUNIT["degree",0.0174532925199433]],
    CS[ellipsoidal,2],
        AXIS["geodetic latitude (Lat)",north,
            ORDER[1],
            ANGLEUNIT["degree",0.0174532925199433]],
        AXIS["geodetic longitude (Lon)",east,
            ORDER[2],
            ANGLEUNIT["degree",0.0174532925199433]],
    ID["EPSG",4326]]
Data axis to CRS axis mapping: 2,1
F_CODE: String (0.0)
ZI001_SDV: DateTime (0.0)
UFI: String (0.0)
ZI005_FNA: String (0.0)
RTY: Integer (0.0)
FCSUBTYPE: Integer (0.0)
RIN_ROI: Integer (0.0)
ZI001_SDP: String (0.0)
ZI016_WTC: Integer (0.0)
RLE: Integer (0.0)
LOC: Integer (0.0)
TRS: Integer (0.0)
```

### Fetch selected features and write them to a CSV or GeoPackage file

The following command

- selects all name features from the OS Open Zoomstack dataset (`OAPIF:https://demo.ldproxy.net/zoomstack names`)
  - between -2° West and 2° East (`-spat -2 45 2 65`)
  - that are cities (`-where "type='City'"`)
  - using a page size of 1000 features (`-oo PAGE_SIZE=1000`)
- convert the coordinates to the British National Grid (`-t_srs EPSG:27700`), and
- writes the features 
  - as a CSV file (`-f CSV cities.csv`) and
  - includes the geometries (`-lco GEOMETRY=AS_XY`).

Note that the debug log shows that GDAL

- at least partially supports Part 3 "Filtering and CQL" (the `where` parameter is not evaluated by GDAL, but passed in the API request as `filter=type%20%3D%20'City'&filter-lang=cql-text`),
- does not support Part 2 "Coordinate Reference Systems by Reference" (the `t_srs` parameter is not used to request the data directly in the British National Grid).

```sh
% ogr2ogr -spat -2 45 2 65 -where "type='City'" -t_srs EPSG:27700 -oo PAGE_SIZE=1000 -lco GEOMETRY=AS_XY -f CSV cities.csv OAPIF:https://demo.ldproxy.net/zoomstack names
% cat cities.csv
X,Y,type,name1
439612.00083496,556556.003708444,City,Sunderland
426946.000836522,542630.003712859,City,Durham
425048.000837868,564892.003704596,City,Newcastle upon Tyne
416267.00083097,432746.003747514,City,Bradford
431236.000831386,471237.003737212,City,Ripon
429719.000828715,433916.003748372,City,Leeds
433242.000826933,420922.003752427,City,Wakefield
460218.000824216,452158.003745674,City,York
411773.000819008,309501.003777365,City,Lichfield
435187.000817871,336492.003774348,City,Derby
435449.00082334,387427.003761794,City,Sheffield
458743.000808943,304337.003784692,City,Leicester
457119.000813732,340206.003776228,City,Nottingham
497650.000807601,371864.00377322,City,Lincoln
406689.000817039,286822.003781248,City,Birmingham
433644.000810956,278970.003786435,City,Coventry
451342.000796432,206181.003802109,City,Oxford
414360.00079145,130135.003805651,City,Salisbury
448380.000783917,129384.003812115,City,Winchester
441982.000782148,111882.00381279,City,Southampton
464148.00077449,100092.003818494,City,Portsmouth
486074.000769549,104818.003822559,City,Chichester
510063.000810144,428869.003757889,City,Kingston upon Hull
514747.000779915,207262.003813069,City,St Albans
519204.000792514,298638.003794757,City,Peterborough
544945.00077867,258410.003807655,City,Cambridge
554027.000778957,280363.0038038,City,Ely
570897.0007613,207155.003821933,City,Chelmsford
530855.000755825,104317.003832087,City,Brighton and Hove
530162.000770395,179670.003820678,City,City of Westminster
532473.000769929,181219.003820829,City,City of London
```

The following command fetches all name features that is one of "Country", "Capital", "City", "Town", "Village", or "Hamlet" and creates a GeoPackage file `places.gpkg` with the features:

```sh
% ogr2ogr -where "type='Country' OR type='Capital' OR type='City' OR type='Town' OR type='Village' OR type='Hamlet'" -oo PAGE_SIZE=10000 -f GPKG places.gpkg OAPIF:https://demo.ldproxy.net/zoomstack names
% ogrinfo -so places.gpkg names

INFO: Open of 'places.gpkg'
      using driver 'GPKG' successful.

Layer name: names
Metadata:
  DESCRIPTION=Use this point layer to render contextual labels on your map.
  TITLE=Names
Geometry: Point
Feature Count: 29435
Extent: (-7.537203, 49.891907) - (1.750427, 60.800102)
Layer SRS WKT:
GEOGCRS["WGS 84",
    DATUM["World Geodetic System 1984",
        ELLIPSOID["WGS 84",6378137,298.257223563,
            LENGTHUNIT["metre",1]]],
    PRIMEM["Greenwich",0,
        ANGLEUNIT["degree",0.0174532925199433]],
    CS[ellipsoidal,2],
        AXIS["geodetic latitude (Lat)",north,
            ORDER[1],
            ANGLEUNIT["degree",0.0174532925199433]],
        AXIS["geodetic longitude (Lon)",east,
            ORDER[2],
            ANGLEUNIT["degree",0.0174532925199433]],
    USAGE[
        SCOPE["Horizontal component of 3D system."],
        AREA["World."],
        BBOX[-90,-180,90,180]],
    ID["EPSG",4326]]
Data axis to CRS axis mapping: 2,1
FID Column = fid
Geometry Column = geom
type: String (0.0)
name1: String (0.0)
name1language: String (0.0)
name2: String (0.0)
name2language: String (0.0)
```

And the following command fetches all local road features that have "Queen" as part of the name and creates a GeoPackage file `queen-roads.gpkg` with the features:

```sh
% ogr2ogr -where "name LIKE '%Queen%'" -oo PAGE_SIZE=10000 -f GPKG queen-roads.gpkg OAPIF:https://demo.ldproxy.net/zoomstack roads_local --debug on
% ogrinfo -so queen-roads.gpkg roads_local

INFO: Open of 'queen-roads.gpkg'
      using driver 'GPKG' successful.

Layer name: roads_local
Metadata:
  DESCRIPTION=Lines representing the road network. A road is defined as a metalled way for vehicles.
  TITLE=Local Roads
Geometry: Line String
Feature Count: 8214
Extent: (-6.384481, 50.114640) - (1.752164, 60.370524)
Layer SRS WKT:
GEOGCRS["WGS 84",
    DATUM["World Geodetic System 1984",
        ELLIPSOID["WGS 84",6378137,298.257223563,
            LENGTHUNIT["metre",1]]],
    PRIMEM["Greenwich",0,
        ANGLEUNIT["degree",0.0174532925199433]],
    CS[ellipsoidal,2],
        AXIS["geodetic latitude (Lat)",north,
            ORDER[1],
            ANGLEUNIT["degree",0.0174532925199433]],
        AXIS["geodetic longitude (Lon)",east,
            ORDER[2],
            ANGLEUNIT["degree",0.0174532925199433]],
    USAGE[
        SCOPE["Horizontal component of 3D system."],
        AREA["World."],
        BBOX[-90,-180,90,180]],
    ID["EPSG",4326]]
Data axis to CRS axis mapping: 2,1
FID Column = fid
Geometry Column = geom
type: String (0.0)
level: Integer (0.0)
name: String (0.0)
```
