from dataclasses import dataclass

@dataclass
class LibUnder:
    lib_name: str
    lib_sources: list[str]

@dataclass
class UnitConfig:
    unit_name: str
    list_sources: list[str]
    lib_source: list[LibUnder]


