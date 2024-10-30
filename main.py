import argparse
import toml
import config_functions  # Importer le module contenant les fonctions de configuration

def parse_overrides(overrides):
    """Convertit les arguments de type --clé.sous_clé=valeur en dictionnaire imbriqué."""
    update_dict = {}
    for override in overrides:
        key_path, value = override.split("=", 1)
        
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass  # Laisser la valeur en tant que chaîne si elle n'est ni un int ni un float
        
        keys = key_path.lstrip("-").split(".")
        d = update_dict
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value

    return update_dict

def deep_update(source, updates):
    """Mise à jour récursive du dictionnaire source avec les valeurs du dictionnaire updates."""
    for key, value in updates.items():
        if isinstance(value, dict) and key in source:
            deep_update(source[key], value)
        else:
            source[key] = value

def main():
    parser = argparse.ArgumentParser(description="Script de configuration avec surcharge via ligne de commande")
    parser.add_argument("config_path", type=str, help="Chemin du fichier de configuration TOML")
    parser.add_argument("overrides", nargs=argparse.REMAINDER, help="Arguments de surcharge au format --clé.sous_clé=valeur")

    args = parser.parse_args()

    # Charger le fichier TOML
    with open(args.config_path, "r") as file:
        config_data = toml.load(file)

    # Analyser et appliquer les overrides
    overrides = parse_overrides(args.overrides)
    deep_update(config_data, overrides)

    # Parcourir chaque section de la configuration et appeler la fonction correspondante
    for section, params in config_data.items():
        # Vérifier si une fonction du même nom existe dans config_functions
        func = getattr(config_functions, section, None)
        if callable(func):
            print(f"Appel de la fonction '{section}' avec les paramètres : {params}")
            func(params)
        else:
            print(f"Aucune fonction trouvée pour la section '{section}'")

if __name__ == "__main__":
    main()
