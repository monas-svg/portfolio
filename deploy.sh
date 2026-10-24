#!/bin/bash
cd /home/ubuntu/portfolio/portfolio
docker compose --env-file /home/ubuntu/secrets/portfolio.env "$@"
