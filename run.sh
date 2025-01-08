cp common-library/dist/*whl price-collector/packages
docker compose -f docker-compose.dev.yml up --build
