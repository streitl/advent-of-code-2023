from pathlib import Path

INPUTS_PATH = Path(__file__).parent.parent.joinpath("inputs")


def load_input(filename: str) -> str:
    return INPUTS_PATH.joinpath(filename).read_text()
