"""This script must be run to refresh the binary data required by this package.
All previous data gets cleared and all existing subclasses of `SentenceEnum` will get their binary data generated."""

import shutil


from typing import Union, Optional

from brontology.utils.spacy import MODEL
from tests.samples.doc.sentence import SentenceEnum, BIN_FOLDER


def main():
    """Runs this script."""
    shutil.rmtree(BIN_FOLDER, ignore_errors=True)
    BIN_FOLDER.mkdir(parents=True)
    for implementation in SentenceEnum.__subclasses__():
        for member in implementation:
            member: SentenceEnum
            doc = MODEL(member.value)
            member.file.parent.mkdir(parents=True, exist_ok=True)
            doc.to_disk(member.file)


if __name__ == "__main__":
    main()
