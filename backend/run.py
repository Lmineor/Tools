from lextool import create_app
from lextool.config.config import Cfg
from lextool.common.logger import LOG

app = create_app()

debug = Cfg.TOOLS.debug

if __name__ == '__main__':
    LOG.info("Running server...")
    app.run(debug=debug)
