from typing import List
from ninja_bear import Property
from ninja_bear.base.generator_configuration import GeneratorConfiguration
from ninja_bear_language_javascript.generator import Generator as JavaScriptGenerator, ExportType

class Generator(JavaScriptGenerator):
    """
    TypeScript specific generator. For more information about the generator methods, refer to GeneratorBase.
    """
    def __init__(self, config: GeneratorConfiguration, properties: List[Property] = ..., additional_props=...):
        super().__init__(config, properties, additional_props)

        # Make sure code is always exported in the style of ESM.
        self.export_type = ExportType.ESM

    # Override JavaScriptGenerator method.
    def _type_start(self, type_name: str) -> str:
        return f'const {type_name} = {{'
    
    # Override JavaScriptGenerator method.
    def _property(self, name: str, value: str):
        return f'{name}: {value},'

    # Override JavaScriptGenerator method.
    def _type_end(self) -> str:
        return '} as const;'
