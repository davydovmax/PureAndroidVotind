#!/usr/bin/python
import config
import logging


if __name__ == '__main__':
    env = config.env = config.Environment()
    logging.getLogger().debug('debug')

    import bottle
    from bottle.ext.sqlalchemy import SQLAlchemyPlugin
    bottle.install(SQLAlchemyPlugin(env.engine, env.Base.metadata, create=True))

    # run server
    import view # required to create routes
    import test_view # required to create routes
    bottle.debug(env.is_debug_mode)
    bottle.run(host='0.0.0.0', port=env.port, reloader=True)