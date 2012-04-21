#!/usr/bin/python
import config


if __name__ == '__main__':
    env = config.env = config.Environment()

    import bottle
    from bottle.ext.sqlalchemy import SQLAlchemyPlugin
    bottle.install(SQLAlchemyPlugin(env.engine, env.Base.metadata, create=True))

    # run server
    from app import  view, test_view # required to create routes
    bottle.debug(env.is_debug_mode)
    bottle.run(host='0.0.0.0', port=env.port, reloader=False)