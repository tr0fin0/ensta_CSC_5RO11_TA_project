# run.py

from __init__ import create_app
from models import create_csv


def main():
    create_csv()

    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
