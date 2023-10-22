from __future__ import annotations

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
from python_tools.util.blackbox import decode_blackbox

USAGE = "Usage: `python decode_blackbox.py <log_path> [<output_path>]`"
HELP_MESSAGE = f"""
    Cross platform script to decode blackbox data.

    {USAGE}
        log_path: path to the blackbox log
        output_path: path to the output csv file. Default is <log_path>.csv
""".strip()


def main(args: list[str]):
    if len(args) < 2 or args[1] == "-h" or args[1] == "--help":
        print(HELP_MESSAGE)
        return
    assert (
        len(args) <= 3
    ), f"Use quotes around file paths with spaces. Try `python decode_blackbox.py --help`. {USAGE}"
    log_path = args[1]
    output_path = args[2] if len(args) > 2 else log_path[:-4] + ".csv"
    df = decode_blackbox(log_path)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main(sys.argv)
