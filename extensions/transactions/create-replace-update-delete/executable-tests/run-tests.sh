#!/usr/bin/env bash
# Executes the tests of the Abstract Test Suite (Annex A) against a local
# ldproxy deployment (see docker-compose.yml). Starts the deployment if it is
# not running, waits until the API is available and runs all applicable tests.
#
# Arguments are passed on to ats/run_ats.py, for example:
#   ./run-tests.sh --only /conf/features
#   ./run-tests.sh --verbose
set -euo pipefail
cd "$(dirname "$0")"

API="http://localhost:7080/buildings"
DATA_DIR="${DATA_DIR:-../standard/data}"
RESET_CMD="docker compose exec -T db psql -q -v ON_ERROR_STOP=1 -U postgres -d buildings -f /docker-entrypoint-initdb.d/21-load.sql"

docker compose up -d --wait 2>/dev/null || docker compose up -d

echo "Waiting for $API ..."
for i in $(seq 1 60); do
  if curl -sf -o /dev/null -H "Accept: application/json" "$API"; then
    break
  fi
  if [ "$i" = 60 ]; then
    echo "ldproxy did not become ready; check: docker compose logs ldproxy" >&2
    exit 2
  fi
  sleep 2
done

# Main pass: the API with CRS support, the collection "buildings" (feature ids
# assigned by the server) as the resource under test and "buildings_upsert"
# (client-assigned ids) for the tests that create features with PUT.
status=0
python3 ats/run_ats.py \
  --landing-page "$API" \
  --collection buildings \
  --put-create-collection buildings_upsert \
  --data-dir "$DATA_DIR" \
  --reset-cmd "$RESET_CMD" \
  "$@" || status=$?

# Second pass: the condition of /conf/features/crs84 is a conformance declaration
# WITHOUT "Coordinate Reference Systems by Reference". The conformance declaration
# is per API, so that test runs against the second API, which does not support
# coordinate reference systems other than WGS 84 longitude/latitude. Skipped if
# the caller restricted the run to other tests.
# The options of the caller are passed on, except the two that the second pass
# sets itself: --only (it runs one test) and --put-create-collection (the second
# API has no collection with client-assigned identifiers).
only=""
passthru=()
expect=""
for arg in "$@"; do
  if [ -n "$expect" ]; then
    case "$expect" in --only) only="$arg" ;; esac
    expect=""
    continue
  fi
  case "$arg" in
    --only|--put-create-collection) expect="$arg" ;;
    --only=*) only="${arg#--only=}" ;;
    --put-create-collection=*) ;;
    *) passthru+=("$arg") ;;
  esac
done
if [ -z "$only" ] || printf '%s' "/conf/features/crs84" | grep -qF -- "$only"; then
  echo
  echo "=== second pass: API without support for other coordinate reference systems ==="
  python3 ats/run_ats.py \
    --landing-page "http://localhost:7080/buildings-nocrs" \
    --collection buildings \
    --data-dir "$DATA_DIR" \
    --reset-cmd "$RESET_CMD" \
    --only /conf/features/crs84 ${passthru[@]+"${passthru[@]}"} || status=$?
fi

exit $status
