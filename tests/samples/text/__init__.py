from pathlib import Path

file_dir: Path = Path(__file__).parent

SAMPLE_1: str = open(file_dir / "sample_1.txt").read()
"""A long text with complex grammar."""
SAMPLE_2: str = open(file_dir / "sample_2.txt").read()
"""A long text with complex grammar, focussing on auxiliary verbs."""
SAMPLE_3: str = open(file_dir / "sample_3.txt").read()
"""A long text with complex grammar, focussing on subordinated and coordinated clauses."""
SAMPLE_4: str = open(file_dir / "sample_4.txt").read()
"""A long text with complex grammar, focussing on passive voice."""
