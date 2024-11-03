import pytest
import toml
from unittest.mock import MagicMock, patch
from main import parse_overrides, deep_update, validate_params, validate_all_params, setup_logger, main
import tempfile
import logging

# Mock configuration functions module since it's imported but not provided
config_functions = MagicMock()

def test_parse_overrides():
    # Test single override with nested keys
    overrides = ["--database.connection_timeout=10", "--database.host='localhost'"]
    result = parse_overrides(overrides)
    assert result == {'database': {'connection_timeout': 10, 'host': 'localhost'}}

    # Test override with multiple nested layers
    overrides = ["--service.api.timeout=30"]
    result = parse_overrides(overrides)
    assert result == {'service': {'api': {'timeout': 30}}}

def test_deep_update():
    source = {'a': 1, 'b': {'c': 2}}
    updates = {'b': {'c': 3, 'd': 4}, 'e': 5}
    deep_update(source, updates)
    assert source == {'a': 1, 'b': {'c': 3, 'd': 4}, 'e': 5}

def test_validate_params():
    # Mock function with specific parameters
    def mock_func(a, b, c=3): pass

    # Valid params
    validate_params(mock_func, {'a': 1, 'b': 2})
    
    # Missing required parameter 'a'
    with pytest.raises(ValueError, match="manque les paramètres obligatoires: {'a'}"):
        validate_params(mock_func, {'b': 2})
    
    # Extra invalid parameter
    with pytest.raises(ValueError, match="paramètres non acceptés pour la fonction 'mock_func'"):
        validate_params(mock_func, {'a': 1, 'b': 2, 'd': 4})

def test_validate_all_params():
    # Mock the config functions and parameters
    with patch("main.config_functions", config_functions):
        # Set up a function with specific parameters
        config_functions.test_section = lambda x, y: x + y
        
        # Valid parameters
        config_data = {"test_section": {"x": 1, "y": 2}}
        assert validate_all_params(config_data) == []

        # Invalid parameter for test_section
        config_data = {"test_section": {"x": 1, "z": 2}}
        errors = validate_all_params(config_data)
        assert "paramètres non acceptés" in errors[0]

def test_main():
    # Use tempfile to create a temporary configuration file
    with tempfile.NamedTemporaryFile("w+", suffix=".toml") as config_file:
        # Write a sample TOML config to the file
        config_data = {
            "global": {"log_level": "DEBUG", "max_connections": 5},
            "test_section": {"param1": "value1"}
        }
        toml.dump(config_data, config_file)
        config_file.seek(0)

        # Patch config_functions and setup_logger to avoid executing real functions
        with patch("main.config_functions", config_functions):
            config_functions.test_section = MagicMock()
            with patch("main.setup_logger") as mock_logger:
                mock_logger.return_value = logging.getLogger("test")
                
                # Run the main function with the temporary config file
                with patch("sys.argv", ["main", config_file.name]):
                    # Mock overrides with no command-line overrides to test file parsing
                    main()

                # Ensure function was called
                config_functions.test_section.assert_called_once_with(param1="value1")

def test_main2():
    # Use tempfile to create a temporary configuration file
    with tempfile.NamedTemporaryFile("w+", suffix=".toml") as config_file:
        # Write a sample TOML config to the file
        config_data = {
            "global": {"log_level": "DEBUG", "max_connections": 5},
            # "test_section": {"param1": "value1"}
        }
        toml.dump(config_data, config_file)
        config_file.seek(0)

        # Patch config_functions and setup_logger to avoid executing real functions
        # with patch("main.config_functions", config_functions):
        #     config_functions.test_section = MagicMock()
            # with patch("main.setup_logger") as mock_logger:
            #     mock_logger.return_value = logging.getLogger("test")
                
        # Run the main function with the temporary config file
        with patch("sys.argv", ["main", config_file.name]):
            # Mock overrides with no command-line overrides to test file parsing
            main()

                # Ensure function was called
    # config_functions.test_section.assert_called_once_with(param1="value1")


