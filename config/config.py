import environs
env = environs.Env()

env.read_env()
import os
token = str(os.environ.get('BOT_TOKEN'))
db_uri = str(os.environ.get('DB_URI'))
admin_list = [6606390277]

