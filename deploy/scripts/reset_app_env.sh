#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${1:-}"
if [[ "$ENV_NAME" != "test" && "$ENV_NAME" != "prod" ]]; then
  echo "Usage: $0 {test|prod}"
  exit 1
fi

APP_DIR="/srv/app-${ENV_NAME}"
COMPOSE_FILE="${APP_DIR}/compose.yml"

echo "[reset] env=${ENV_NAME}"
echo "[reset] app_dir=${APP_DIR}"
echo "[reset] compose=${COMPOSE_FILE}"

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "[reset] compose file not found: $COMPOSE_FILE"
  echo "[reset] nothing to stop."
else
  echo "[reset] stopping containers..."
  docker compose -f "$COMPOSE_FILE" down --remove-orphans || true
fi

echo "[reset] removing exited containers (global)..."
docker container prune -f || true

echo "[reset] removing dangling images (global)..."
docker image prune -f || true

echo "[reset] removing build cache (global, safe)..."
docker builder prune -f || true

echo "[reset] optional: clean old tar files in /tmp for this env"
rm -f "/tmp/base-images-${ENV_NAME}-"*.tar || true

echo "[reset] DONE. Data directories under ${APP_DIR}/data are untouched."
