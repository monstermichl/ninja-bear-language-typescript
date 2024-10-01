from typing import List
from ninja_bear import GeneratorBase, Property, NamingConventionType


class Generator(GeneratorBase):
    """
    TypeScript specific generator. For more information about the generator methods, refer to GeneratorBase.
    """

    def _default_type_naming_convention(self) -> NamingConventionType:
        raise Exception('_default_type_naming_convention method not implemented')
    
    def _line_comment(self, string: str) -> str:
        raise Exception('_line_comment method not implemented')
    
    def _dump(self, type_name: str, properties: List[Property]) -> str:
        raise Exception('_dump method not implemented')
