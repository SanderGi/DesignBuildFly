from __future__ import annotations
import pandas as pd
import zipfile
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
from python_tools.util.thrust import decode_thrust

USAGE = "Usage: `python decode_thrust.py <zip_path> [<output_path>]`"
HELP_MESSAGE = f"""
    Parses zipped txt files with thrust values into csv files (one per overall run with columns for battery, prop, motor, and average maximum thrust).

    {USAGE}
        zip_path: path to the zip file containing the txt files. Each text file should follow the naming convention <motor>_<prop>_<battery>_<run_name>.txt
        output_path: path to the output zip file of CSVs. Default is <zip_path>_csvs.zip
""".strip()


def main(args: list[str]):
    if len(args) < 2 or args[1] == "-h" or args[1] == "--help":
        print(HELP_MESSAGE)
        return
    assert (
        len(args) <= 3
    ), f"Use quotes around file paths with spaces. Try `python decode_thrust.py --help`. {USAGE}"

    zip_path = args[1]
    output_path = args[2] if len(args) > 2 else zip_path[:-4] + "_csvs.zip"

    run_dfs = decode_thrust(zip_path)

    with zipfile.ZipFile(output_path, "w") as zipped_f:
        for run_name, run_df in run_dfs.items():
            run_df: pd.DataFrame
            print(run_name)
            print(run_df.head())
            zipped_f.writestr(run_name + ".csv", run_df.to_string(index=False))


if __name__ == "__main__":
    main(sys.argv)
