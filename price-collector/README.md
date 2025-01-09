curl http://localhost:37967/api/stocks/kr/005930


curl -X POST http://localhost:37967/jobs/candels/kr


cp ../common-library/dist/*whl packages
pip install packages/*.whl --force-reinstall

docker exec -it b73436688f4f bash
show dbs

use stockdb
db.stock_kr.find()

