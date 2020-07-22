from lextool import create_app
from lextool.config.local_config import DEV

app = create_app()


if __name__ == '__main__':
    app.run(debug=DEV)
