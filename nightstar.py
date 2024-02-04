import argparse
import logging
from pathlib import Path

from src.unpacker import Unpacker

logging.basicConfig()
LOGGER = logging.getLogger("nightstar")
LOGGER.setLevel(logging.INFO)


def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    # UNPACK
    unpack = subparsers.add_parser("unpack")
    unpack.add_argument(
        "-root",
        dest="root",
        type=Path,
        required=True,
        help="Parent directory containing desired translation files",
    )
    unpack.add_argument(
        "-out",
        dest="path_corpus",
        type=Path,
        required=True,
        help="Desired path for output corpus file",
    )

    # TRANSLATE
    translate = subparsers.add_parser("translate")
    translate.add_argument(
        "-raw",
        help="Corpus text file to be translated (line by line)",
        dest="file_raw",
        type=Path,
        required=True,
    )
    translate.add_argument(
        "-translate",
        help="Output file to store translated text (line by line)",
        type=Path,
        dest="file_translate",
        required=True,
    )
    translate.add_argument(
        "-ls",
        "--line_start",
        help="Line number with which to start processing (inclusive)",
        dest="line_start",
        type=int,
        default=0,
        required=False,
    )
    translate.add_argument(
        "-le",
        "--line_end",
        help="Line number with which to stop processing (exclusive)",
        dest="line_end",
        type=int,
        required=False,
    )

    # REPACK
    repack = subparsers.add_parser("repack")
    repack.add_argument(
        "-root",
        type=Path,
        help="Parent directory containing untranslated files",
    )
    repack.add_argument(
        "-translate",
        type=Path,
        help="Translated corpus file to be repacked",
    )

    params = vars(parser.parse_args())
    dispatch(params)


def dispatch(params: dict):
    action = params.pop("action")
    LOGGER.info(f"NightStar Action: {action}")
    if action == "unpack":
        LOGGER.info(f"Executing Unpacker...")
        unpacker = Unpacker(**params)
        unpacker.unpack()
    elif action == "translate":
        LOGGER.error(f"To Be Implemented: {action}")
        pass
    elif action == "repack":
        LOGGER.error(f"To Be Implemented: {action}")
        pass
    else:
        LOGGER.error(
            f"Unsupported action '{action}'. "
            f"Supported Actions: [unpack, repack, translate]")


if __name__ == "__main__":
    run()
