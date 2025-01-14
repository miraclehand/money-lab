source venv/bin/activate
source ../.env
python setup.py sdist bdist_wheel
cp dist/*whl ../price-collector/packages
cp dist/*whl ../disclosure-collector/packages
cp dist/*whl ../strategy-module/packages
cp dist/*whl ../simulation-engine/packages
