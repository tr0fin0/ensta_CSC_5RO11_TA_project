# run.py

from app import create_app
from app.models import create_csv


def main():
    create_csv()

    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
