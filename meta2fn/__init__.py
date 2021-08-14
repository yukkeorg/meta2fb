"""[summary]

"""
__version__ = '0.1.0'


def cli() -> None:
    import os
    import logging
    from argparse import ArgumentParser
    from meta2fn.metadatarenamer import MetadataRenamer, DoNotRenameError

    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"),
                        format="[%(levelname)-7s] %(message)s")

    parser = ArgumentParser()
    parser.add_argument("--format", "-f", required=True)
    parser.add_argument("--dryrun", "-n", action="store_true")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    if args.dryrun:
        logging.info("** DRYRUN MODE : Rename is not work. **")

    renamer = MetadataRenamer(args.format, args.dryrun)
    for p in args.paths:
        try:
            renamer.rename(p)
        except DoNotRenameError as e:
            logging.warning("Do not renamed. reason: " + str(e))


if __name__ == "__main__":
    cli()