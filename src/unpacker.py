import logging
from pathlib import Path
from typing import Iterator, List, Match

from src import repl as rp
from src import regex as rx
from src.util import get_file_paths
LOGGER = logging.getLogger("nightstar")


class Unpacker:
    def __init__(self, root: Path, path_corpus: Path):
        self.filepaths: List[Path] = get_file_paths(root, ".xml")
        self.path_corpus = path_corpus
        self.current_file: Path = None

    def unpack(self):
        LOGGER.info(f"{self.__class__.__name__} Starting...")
        with open(self.path_corpus, "w", encoding="windows-1251") as fp:
            fp.write("--- NIGHTSTAR CORPUS FILE ---\n\n")

        for filepath in self.filepaths:
            self.current_file = filepath
            LOGGER.debug(f"|{filepath.name}| Processing...")

            with open(filepath, "r", encoding="windows-1251") as fp:
                content_raw = fp.readlines()

            content = self.parse_file_content(content_raw)
            if not content:
                LOGGER.debug(f"|{filepath.name}| Nothing to Unpack")
                continue

            header = "|FILE|" + filepath.absolute().name + "\n"
            content.insert(0, header)
            LOGGER.info(f"|{filepath.name}| Unpacked Successfully")

            with open(self.path_corpus, "a", encoding="windows-1251") as fp:
                fp.writelines(line + "\n" for line in content)
                fp.write("\n")

    def parse_file_content(self, content_raw: List[str]) -> List[str]:
        content = []
        
        current_id = None
        line_iter: Iterator[str] = iter(content_raw)
        for line in line_iter:
            line = line.strip()

            if line.startswith("<!--"):
                content.append(line)
                continue
            if line == "":
                content.append(line)
                continue

            match_id = rx.XML_ID.search(line)
            match_text_simple = rx.XML_TEXT_SIMPLE.search(line)
            match_text_multiline = rx.XML_TEXT_MULTILINE_START.search(line)

            if match_id:
                current_id = match_id.groups()[0]

            text_unpacked = None
            if match_text_simple:
                LOGGER.debug(f"|{self.current_file}| [{current_id}] Match - Simple")
                text_unpacked = match_text_simple.groups()[0]
            elif match_text_multiline:
                LOGGER.debug(f"|{self.current_file}| [{current_id}] Match - Multiline")
                text_unpacked = self.process_multiline_match(line_iter, match_text_multiline)
          
            if text_unpacked:
                for repl_item, repl_value in rp.BASE.items():
                    text_unpacked = text_unpacked.replace(repl_item, repl_value)

                line_parsed = f"<{current_id}>{text_unpacked}"
                content.append(line_parsed)

        return content

    @staticmethod
    def process_multiline_match(line_iter: Iterator, match: Match) -> str:
        text_unpacked: List[str] = []

        # Handle Starting Line
        LOGGER.debug(f"Match - Multiline: Start")
        text_multiline_start = match.groups()[0]
        text_unpacked.append(text_multiline_start)

        # Handle Middle Line(s)
        line = next(line_iter)
        while not rx.XML_TEXT_MULTILINE_END.search(line):
            LOGGER.debug(f"Match - Multiline: General")
            text_unpacked.append(line[:-1])  # Strip out last newline char
            line = next(line_iter)

        # Handle End Line
        match_end = rx.XML_TEXT_MULTILINE_END.search(line)
        text_multiline_end = match_end.groups()[0]
        if text_multiline_end:
            LOGGER.debug("Match - Multiline: End")
            text_unpacked.append(text_multiline_end)

        text_unpacked_flattened = rp.NEWLINE_XML.join(text_unpacked)
        return text_unpacked_flattened
