#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[portfolio] Démarrage des conteneurs..."
docker compose up -d --build --force-recreate

echo "[portfolio] Vérification de la santé de l'application..."
for i in $(seq 1 30); do
  if curl -fsS http://localhost:8080/ >/dev/null 2>&1; then
    echo "[portfolio] Application accessible sur http://localhost:8080/"
    exit 0
  fi
  echo "[portfolio] En attente du service... (${i}/30)"
  sleep 2
done

echo "[portfolio] L'application n'est pas accessible après le redémarrage." >&2
exit 1
