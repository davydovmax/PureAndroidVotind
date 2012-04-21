import os
import sys
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger('srv.'+__name__)


class HistoryHandler(logging.Handler):
    """Captures and stores log records, 128 by default."""
    def __init__(self, level=logging.NOTSET, max_records=128):
        """Constructor."""
        super(HistoryHandler, self).__init__(level=logging.NOTSET)
        self.records = []
        self.max_records = max_records
        self.lock = None

    def handle(self, record):
        """Handles and saves log record to memory."""
        self.emit(record)

    def emit(self, record):
        """Handles and saves log record to memory."""
        trim = len(self.records) - self.max_records
        if trim > 0:
            del self.records[0:trim]
        self.records.append(record)

    def createLock(self):
        self.lock = None


class Environment(object):
    is_debug_mode = True
    is_db_echo = True
    is_production = False
    port = 5000
    db_url = 'sqlite:///votes.db'
    history = HistoryHandler()
    Base = None
    engine = None
    create_session = None

    def __init__(self):
        """Constructor."""
        self._config()
        self._init_logging()
        self._log_configuration()
        self._initialize_db()

    def _config(self):
        """Gets configuration data from environment."""
        self.is_production = True if os.environ.get('PROD') else False
        self.port = int(os.environ.get('PORT', self.port))
        self.db_url = os.environ.get('DATABASE_URL') or self.db_url

    def _init_logging(self):
        """Initializes logging and attach log filter."""
        logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        loggers = [logging.getLogger('bottle.starter'),
                   logging.getLogger('sqlalchemy'),
                   logging.getLogger('srv')]

        logger_level = logging.DEBUG if self.is_debug_mode else logging.WARNING
        for l in loggers:
            l.setLevel(logger_level)
            l.addHandler(self.history)

        # add some text to log
        logger.info('Logger initialized')

    def _log_configuration(self):
        """Log some config data."""
        logger.info('Debug mode: %s' % self.is_debug_mode)
        logger.info('DB echo: %s' % self.is_db_echo)
        logger.info('Production environment: %s' % self.is_production)
        logger.info('Port: %s' % self.port)
        logger.info('Database url: %s' % self.db_url)


    def _initialize_db(self):
        """Initialize sqlalchemy."""
        logger.info('Initializing database')
        self.Base = declarative_base()
        self.engine = create_engine(self.db_url, echo=self.is_db_echo)
        self.create_session = sessionmaker(bind=self.engine)
