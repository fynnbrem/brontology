from pathlib import Path
# noinspection PyUnresolvedReferences
from typing import Union, Optional

file_dir: Path = Path(__file__).parent

SAMPLE_1: str = open(file_dir / "sample_1.txt").read()
"""A long text with complex grammar."""
SAMPLE_2: str = open(file_dir / "sample_1.txt").read()
"""A long text with complex grammar, focussing on auxiliary verbs."""
SAMPLE_3: str = open(file_dir / "sample_1.txt").read()
"""A long text with complex grammar, focussing on subordinated and coordinated clauses."""
