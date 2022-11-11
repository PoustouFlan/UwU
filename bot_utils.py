from yaml import safe_load

configuration_file = open("configuration.yaml", "r")
configuration = safe_load(configuration_file.read())

TOKEN = configuration['token']
GUILD_ID = configuration['guild_id']