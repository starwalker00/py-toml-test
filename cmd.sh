#!/bin/bash

# Commande pour exécuter le script Python avec le fichier de configuration
python main.py config.toml

# Exécution avec des paramètres supplémentaires
python main.py config.toml --database.port="1111" --database.username=new_user

# Ajoutez d'autres commandes d'exécution selon vos besoins
python main.py config.toml --aaa.param1=valeur1
