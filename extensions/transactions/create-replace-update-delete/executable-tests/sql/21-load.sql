-- (Re-)load the test dataset. Idempotent: run at initdb time and to reset
-- the data between test runs. Keeps the "updated" values from the dataset
-- (the trigger only assigns now() when the value is missing or on UPDATE).

ALTER SEQUENCE buildings_id_seq RESTART WITH 100;

TRUNCATE buildings;

INSERT INTO buildings (id, name, function, height, updated, geom) VALUES
('B.1', 'City Hall', 'public', 16.5, '2026-07-14T09:30:00Z',
 ST_Transform(ST_SetSRID(ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[8.708,49.412],[8.7084,49.412],[8.7084,49.4123],[8.708,49.4123],[8.708,49.412]]]}'),4326),25832)),
('B.2', 'Old Mill', 'commercial', 9.0, '2026-07-21T14:45:00Z',
 ST_Transform(ST_SetSRID(ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[8.7091,49.4127],[8.7095,49.4127],[8.7095,49.413],[8.7091,49.413],[8.7091,49.4127]]]}'),4326),25832)),
('B.3', 'Rose Cottage', 'residential', 7.2, '2026-08-02T08:05:00Z',
 ST_Transform(ST_SetSRID(ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[8.7102,49.4114],[8.7106,49.4114],[8.7106,49.4117],[8.7102,49.4117],[8.7102,49.4114]]]}'),4326),25832));

TRUNCATE buildings_upsert;

INSERT INTO buildings_upsert (id, name, function, height, updated, geom)
  SELECT id, name, function, height, updated, geom FROM buildings;
