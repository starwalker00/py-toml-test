# config_functions.py

def database(config):
    print(f"Connecting to database at {config['server']} on port {config['port']}")
    print(f"Username: {config['username']}")
    # Code de connexion à la base de données ici

def aaa(config):
    print(f"Function 'aaa' called with config: {config}")
    # Traitement spécifique à aaa

def bbb(config):
    print(f"Function 'bbb' called with config: {config}")
    # Traitement spécifique à bbb
