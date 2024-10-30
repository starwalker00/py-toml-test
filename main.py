import argparse
import toml
import inspect
import logging
import config_functions  # Importer le module contenant les fonctions de configuration

# Configuration du logger
def setup_logger(log_level):
    """Configure le logger."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def parse_overrides(overrides):
    """Convertit les arguments de type --clé.sous_clé=valeur en dictionnaire imbriqué."""
    update_dict = {}
    for override in overrides:
        key_path, value = override.split("=", 1)
        
        # Conversion du type de la valeur
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass  # Laisser la valeur en tant que chaîne si elle n'est ni un int ni un float
        
        # Création du dictionnaire imbriqué
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

def validate_params(func, params):
    """Vérifie que tous les paramètres fournis sont acceptés par la fonction, et que les obligatoires sont présents."""
    sig = inspect.signature(func)
    accepted_params = set(sig.parameters.keys())
    provided_params = set(params.keys())
    
    # Trouver les paramètres non acceptés
    invalid_params = provided_params - accepted_params
    if invalid_params:
        raise ValueError(f"Les paramètres non acceptés pour la fonction '{func.__name__}': {invalid_params}")

    # Vérifier les paramètres obligatoires
    required_params = {key for key, value in sig.parameters.items() if value.default is inspect.Parameter.empty}
    missing_required = required_params - provided_params
    if missing_required:
        raise ValueError(f"Fonction '{func.__name__}' manque les paramètres obligatoires: {missing_required}")

def validate_all_params(config_data):
    """Valide tous les paramètres pour chaque fonction de configuration. Retourne une liste d'erreurs."""
    errors = []
    for section, params in config_data.items():
        # Vérifier si une fonction du même nom existe dans config_functions
        func = getattr(config_functions, section, None)
        if callable(func):
            try:
                validate_params(func, params)
            except ValueError as e:
                errors.append(str(e))
        else:
            errors.append(f"Aucune fonction trouvée pour la section '{section}'")
    return errors

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

    # Extraire la section 'global' après avoir appliqué les overrides
    global_config = config_data.pop('global', {})  # Supprime la section 'global' et la stocke
    log_level = global_config.get('log_level', 'INFO').upper()  # Valeur par défaut à 'INFO'
    max_connections = global_config.get('max_connections', 10)  # Valeur par défaut à 10

    # Configurer le logger
    logger = setup_logger(log_level)
    logger.info(f"Niveau de log global: {log_level}")
    logger.info(f"Nombre maximal de connexions: {max_connections}")

    # Valider tous les paramètres avant d'appeler les fonctions
    errors = validate_all_params(config_data)
    if errors:
        # Afficher toutes les erreurs sans exécuter les fonctions
        for error in errors:
            logger.error(f"Erreur : {error}")
        raise ValueError("Des paramètres non valides ont été détectés dans la configuration.")
    
    # Si tout est valide, appeler les fonctions
    for section, params in config_data.items():
        func = getattr(config_functions, section, None)
        if callable(func):
            logger.info(f"Appel de la fonction '{section}' avec les paramètres : {params}")
            func(**params)

if __name__ == "__main__":
    main()
