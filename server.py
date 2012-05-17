#!/usr/bin/python
import config


if __name__ == '__main__':
    env = config.env = config.Environment()

    import bottle
    from bottle.ext.sqlalchemy import SQLAlchemyPlugin
    bottle.install(SQLAlchemyPlugin(env.engine, env.Base.metadata, create=True))

    # required to create routes
    from app import view, test_view
    bottle.debug(env.is_debug_mode)

    # run server
    bottle.run(host='0.0.0.0', port=env.port, reloader=False)