import argparse
import toml

def parse_overrides(overrides):
    """Convertit les arguments de type --clé.sous_clé=valeur en dictionnaire imbriqué"""
    update_dict = {}
    for override in overrides:
        # Séparer clé et valeur par le premier signe "="
        key_path, value = override.split("=", 1)
        
        # Convertir la valeur en type approprié (int, float, str) si possible
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass  # Reste une string si ce n'est pas un nombre
        
        # Gérer les clés imbriquées comme database.port
        keys = key_path.lstrip("-").split(".")
        
        # Créer une référence temporaire au dictionnaire
        d = update_dict
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value

    return update_dict

def deep_update(source, updates):
    """Mise à jour récursive du dictionnaire source avec les valeurs du dictionnaire updates"""
    for key, value in updates.items():
        if isinstance(value, dict) and key in source:
            deep_update(source[key], value)
        else:
            source[key] = value

def main():
    parser = argparse.ArgumentParser(description="Script de configuration avec surcharge via ligne de commande")
    parser.add_argument("config_path", type=str, help="Chemin du fichier de configuration TOML")
    parser.add_argument("overrides", nargs="*", help="Arguments de surcharge au format --clé.sous_clé=valeur")

    args = parser.parse_args()

    # Charger le fichier TOML
    with open(args.config_path, "r") as file:
        config_data = toml.load(file)

    # Analyser et appliquer les overrides
    overrides = parse_overrides(args.overrides)
    deep_update(config_data, overrides)

    # Afficher la configuration finale (ou sauvegarder dans un fichier si nécessaire)
    print(toml.dumps(config_data))

if __name__ == "__main__":
    main()
