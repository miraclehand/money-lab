source venv/bin/activate
python setup.py sdist bdist_wheel
cp dist/*whl ../price-collector/packages
