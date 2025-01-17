source venv/bin/activate
source ../.env
python setup.py sdist bdist_wheel
cp dist/*whl ../celery_service/packages
cp dist/*whl ../price_collector_service/packages
cp dist/*whl ../disclosure_collector_service/packages
cp dist/*whl ../strategy_module/packages
cp dist/*whl ../simulation_service/packages

