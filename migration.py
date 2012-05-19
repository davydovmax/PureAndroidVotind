#!/usr/bin/python
from sqlalchemy import MetaData

import config

if __name__ == '__main__':
    env = config.env = config.Environment()
    meta = MetaData(env.engine)
    meta.reflect()
    meta.drop_all()

