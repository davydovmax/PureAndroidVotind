import os


engine = None
create_session = None
Base = None
is_production = os.environ.get('PROD')
db_url = os.environ.get('DATABASE_URL') or 'sqlite:///votes.db'