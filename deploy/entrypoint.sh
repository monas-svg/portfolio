#!/bin/sh
set -e

echo "[entrypoint] Application des migrations..."
python manage.py migrate --noinput

echo "[entrypoint] Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

if [ "$SEED_PORTFOLIO_ON_START" = "true" ]; then
  echo "[entrypoint] Peuplement du contenu initial du portfolio..."
  python manage.py seed_portfolio
fi

echo "[entrypoint] Démarrage : $*"
exec "$@"
