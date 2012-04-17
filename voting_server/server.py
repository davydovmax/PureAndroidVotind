#!/usr/bin/python
import os
import bottle
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

config.Base = declarative_base()
config.engine = create_engine('sqlite:///votes.db', echo=True)
bottle.install(SQLAlchemyPlugin(config.engine, config.Base.metadata, create=True))
config.create_session = sessionmaker(bind=config.engine)

# run server
import view
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bottle.debug(True)
    bottle.run(host='0.0.0.0', port=port, reloader=True)