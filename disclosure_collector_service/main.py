import os
from app import run_app

app = run_app()

if __name__ == '__main__':
    host = os.getenv('DISCLOSURE_IP', 'localhost')
    port = os.getenv('DISCLOSURE_PORT', '8081')

    app.run(host=host, port=port, debug=True)
    #완료 20150101/20191231
