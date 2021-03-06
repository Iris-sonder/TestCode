import sys
import types
from _typeshed import StrOrBytesPath
from abc import ABCMeta, abstractmethod
from importlib.machinery import ModuleSpec
from typing import IO, Any, Iterator, Mapping, Protocol, Sequence, Tuple, Union
from typing_extensions import Literal, runtime_checkable

_Path = Union[bytes, str]

class Finder(metaclass=ABCMeta): ...

class ResourceLoader(Loader):
    @abstractmethod
    def get_data(self, path: _Path) -> bytes: ...

class InspectLoader(Loader):
    def is_package(self, fullname: str) -> bool: ...
    def get_code(self, fullname: str) -> types.CodeType | None: ...
    def load_module(self, fullname: str) -> types.ModuleType: ...
    @abstractmethod
    def get_source(self, fullname: str) -> str | None: ...
    def exec_module(self, module: types.ModuleType) -> None: ...
    @staticmethod
    def source_to_code(data: bytes | str, path: str = ...) -> types.CodeType: ...

class ExecutionLoader(InspectLoader):
    @abstractmethod
    def get_filename(self, fullname: str) -> _Path: ...
    def get_code(self, fullname: str) -> types.CodeType | None: ...

class SourceLoader(ResourceLoader, ExecutionLoader, metaclass=ABCMeta):
    def path_mtime(self, path: _Path) -> float: ...
    def set_data(self, path: _Path, data: bytes) -> None: ...
    def get_source(self, fullname: str) -> str | None: ...
    def path_stats(self, path: _Path) -> Mapping[str, Any]: ...

# Please keep in sync with sys._MetaPathFinder
class MetaPathFinder(Finder):
    def find_module(self, fullname: str, path: Sequence[_Path] | None) -> Loader | None: ...
    def invalidate_caches(self) -> None: ...
    # Not defined on the actual class, but expected to exist.
    def find_spec(
        self, fullname: str, path: Sequence[_Path] | None, target: types.ModuleType | None = ...
    ) -> ModuleSpec | None: ...

class PathEntryFinder(Finder):
    def find_module(self, fullname: str) -> Loader | None: ...
    def find_loader(self, fullname: str) -> Tuple[Loader | None, Sequence[_Path]]: ...
    def invalidate_caches(self) -> None: ...
    # Not defined on the actual class, but expected to exist.
    def find_spec(self, fullname: str, target: types.ModuleType | None = ...) -> ModuleSpec | None: ...

class Loader(metaclass=ABCMeta):
    def load_module(self, fullname: str) -> types.ModuleType: ...
    def module_repr(self, module: types.ModuleType) -> str: ...
    def create_module(self, spec: ModuleSpec) -> types.ModuleType | None: ...
    # Not defined on the actual class for backwards-compatibility reasons,
    # but expected in new code.
    def exec_module(self, module: types.ModuleType) -> None: ...

class _LoaderProtocol(Protocol):
    def load_module(self, fullname: str) -> types.ModuleType: ...

class FileLoader(ResourceLoader, ExecutionLoader, metaclass=ABCMeta):
    name: str
    path: _Path
    def __init__(self, fullname: str, path: _Path) -> None: ...
    def get_data(self, path: _Path) -> bytes: ...
    def get_filename(self, name: str | None = ...) -> _Path: ...
    def load_module(self, name: str | None = ...) -> types.ModuleType: ...

if sys.version_info >= (3, 7):
    class ResourceReader(metaclass=ABCMeta):
        @abstractmethod
        def open_resource(self, resource: StrOrBytesPath) -> IO[bytes]: ...
        @abstractmethod
        def resource_path(self, resource: StrOrBytesPath) -> str: ...
        @abstractmethod
        def is_resource(self, name: str) -> bool: ...
        @abstractmethod
        def contents(self) -> Iterator[str]: ...

if sys.version_info >= (3, 9):
    @runtime_checkable
    class Traversable(Protocol):
        @abstractmethod
        def iterdir(self) -> Iterator[Traversable]: ...
        @abstractmethod
        def read_bytes(self) -> bytes: ...
        @abstractmethod
        def read_text(self, encoding: str | None = ...) -> str: ...
        @abstractmethod
        def is_dir(self) -> bool: ...
        @abstractmethod
        def is_file(self) -> bool: ...
        @abstractmethod
        def joinpath(self, child: _Path) -> Traversable: ...
        @abstractmethod
        def __truediv__(self, child: _Path) -> Traversable: ...
        @abstractmethod
        def open(self, mode: Literal["r", "rb"] = ..., *args: Any, **kwargs: Any) -> IO[Any]: ...
        @property
        @abstractmethod
        def name(self) -> str: ...
