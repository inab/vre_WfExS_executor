from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class Argument:
    name: str
    description: str
    help: Optional[str]
    type: str
    default: Optional[Any] = None


@dataclass
class Cloud:
    launcher: str
    workflow_type: str
    minimum_v_ms: int
    initial_v_ms: int
    default_cloud: bool


@dataclass
class Clouds:
    mug_irb: Cloud


@dataclass
class Infrastructure:
    memory: int
    cpus: int
    executable: str
    clouds: Clouds


@dataclass
class InputFile:
    name: str
    description: str
    help: Optional[str]
    file_type: List[str]
    data_type: List[str]
    required: bool
    allow_multiple: bool


@dataclass
class InputFilesCombination:
    description: Optional[str]
    input_files: List[str]


@dataclass
class MetaData:
    visible: bool
    description: str


@dataclass
class File:
    file_type: str
    data_type: str
    meta_data: MetaData
    file_path: Optional[str] = None
    compressed: Optional[str] = None


@dataclass
class OutputFile:
    name: str
    required: bool
    allow_multiple: bool
    file: File


@dataclass
class Owner:
    author: str
    institution: str
    contact: str
    url: str


@dataclass
class Tool:
    id: str
    name: str
    title: str
    short_description: str
    long_description: str
    url: str
    publication: Optional[str]
    owner: Owner
    keywords: List[str]
    keywords_tool: List[str]
    status: int
    infrastructure: Infrastructure
    input_files: List[InputFile]
    input_files_public_dir: List[Any]
    input_files_combinations: List[InputFilesCombination]
    arguments: List[Argument]
    has_custom_viewer: bool
    output_files: List[OutputFile]
