import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    host = os.getenv('COLLECTOR_IP', 'localhost')
    port = os.getenv('COLLECTOR_PORT', '8080')

    app.run(host=host, port=port, debug=True)
