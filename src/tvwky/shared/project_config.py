import yaml
from typing import Dict, Any


class GetConfig:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_config(config_path: str) -> Dict[str, Any]:
        """
        Function for loading a configuration file.

        Parameters
        ----------
        config_path : str
            The path to the configuration file, from class instantiation.

        Returns
        -------
        dict
            The dictionary constructed from the yaml input file.
        """
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
