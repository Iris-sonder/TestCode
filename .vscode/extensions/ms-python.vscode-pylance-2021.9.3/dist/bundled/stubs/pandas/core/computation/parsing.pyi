import tokenize
from typing import Iterator, Tuple

BACKTICK_QUOTED_STRING: int

def create_valid_python_identifier(name: str) -> str: ...
def clean_backtick_quoted_toks(tok: Tuple[int, str]) -> Tuple[int, str]: ...
def clean_column_name(name: str) -> str: ...
def tokenize_backtick_quoted_string(token_generator: Iterator[tokenize.TokenInfo], source: str, string_start: int) -> Tuple[int, str]: ...
def tokenize_string(source: str) -> Iterator[Tuple[int, str]]: ...
