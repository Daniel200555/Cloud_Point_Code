
import yaml

from config.models import UnitConfig,LibUnder

class ConfigLoader:

    def load(self, yaml_content: str) -> UnitConfig:
        data = yaml.safe_load(yaml_content)

        return UnitConfig(
            unit_name=data['unit_name'],
            list_sources=data['list_sources'],
            lib_source=[
                LibUnder(
                    lib_name=lib['lib_name'],
                    lib_sources=lib['data_sources']
                )
                for lib in data['lib_sources']
            ]
        )