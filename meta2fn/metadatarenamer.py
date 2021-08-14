import logging
from pathlib import Path
from typing import Any, Union

import mutagen   # type: ignore


logger = logging.getLogger(__name__)


class DoNotRenameError(Exception):
    """ Exception class for MetadataRenamer
    """
    ...


class MetadataRenamer:
    def __init__(self, format: str, dryrun: bool=True):
        """ Constractor

        Args:
            format (str): template for to rename.
            dryrun (bool, optional): dryrun mode flag. Defaults to True.
        """
        self.format = format
        self.dryrun = dryrun

    def rename(self, path: Union[Path, str]) -> None:
        """ rename filename with metadata

        Args:
            path (Union[Path, str]): file path for renamed.

        Raises:
            DoNotRenameError: raises when do not renamed.
        """
        if isinstance(path, str):
            path = Path(path)

        try:
            metadata = mutagen.File(str(path))
        except mutagen.MutagenError as e:
            raise DoNotRenameError(str(e))

        logger.debug(metadata)
        logger.info("Origin: " + str(path))

        try:
            target = path.with_stem(self.format.format(**metadata))
        except KeyError as e:
            raise DoNotRenameError("{} is not exist in metadata.".format(str(e)))

        if not self.dryrun:
            path.rename(target)
        logger.info("Renamed: " + str(target))