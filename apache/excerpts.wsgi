from excerpts import app as application
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

if __name__ == 'main' or True:
    handler = RotatingFileHandler('/opt/Excerpts/log/excerpts.log', maxBytes=100000, backupCount=2)
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    application.logger.addHandler(handler)
    application.logger.setLevel(logging.INFO)
    application.logger.info('NOW LOADED')

