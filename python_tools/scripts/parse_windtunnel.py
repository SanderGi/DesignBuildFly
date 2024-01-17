from __future__ import annotations
import zipfile
import pandas as pd
import os
from io import StringIO
import tempfile
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
from python_tools.util.blackbox import decode_blackbox

USAGE = "Usage: `python parse_windtunnel.py <blackbox_zip_path> <wind_tunnel_zip_path> <output_zip_path>`"
HELP_MESSAGE = f"""
    This script combines the blackbox data with the wind tunnel data. It matches test points based on the throttle steps in the blackbox data.
    File names must have the format at5220_15x14x3_40ms_8s_2.4ah_run1.[TXT|csv]

    {USAGE}
        blackbox_zip_path: Path to the blackbox log files (zip) - these are the files that end in .TXT
        wind_tunnel_zip_path: Path to the wind tunnel csv files (zip)
        output_zip_path: Path to the output processed csv files (zip)
        
""".strip()

MIN_THROTTLE = 1065
MAX_THROTTLE = 2011

BLACKBOX_COLS = ["throttle", "escRPM", "amperage (A)", "vbat (V)"]
THRUST_COLS = ["DYNAMIC PRESSURE", "Lift", "Drag"]
METADATA = ["motor", "prop", "airspeed", "cells", "battery", "run"]


def main(args):
    if len(args) < 4 or args[1] == "-h" or args[1] == "--help":
        print(HELP_MESSAGE)
        return
    assert (
        len(args) <= 4
    ), f"Use quotes around file paths with spaces. Try `python parse_data.py --help`. {USAGE}"
    BLACKBOX_ZIP = args[1]
    WINDTUNNEL_ZIP = args[2]
    OUTPUT_ZIP = args[3]

    thrust_dfs: dict[str, pd.DataFrame] = {}
    with zipfile.ZipFile(WINDTUNNEL_ZIP) as z:
        for name in filter(
            lambda x: x.endswith(".csv") and not x.startswith("__MACOSX"), z.namelist()
        ):
            data = z.read(name)
            df = pd.read_csv(StringIO(data.decode("utf-8")))
            df = df[df.CODE == 0]
            df.reset_index(inplace=True, drop=True)
            thrust_dfs[name.replace(".csv", "").split("/")[-1].lower()] = df  # type: ignore

    blackbox_dfs: dict[str, pd.DataFrame] = {}
    with zipfile.ZipFile(BLACKBOX_ZIP) as z:
        for name in filter(
            lambda x: x.endswith(".TXT") and not x.startswith("__MACOSX"), z.namelist()
        ):
            with tempfile.TemporaryDirectory() as tmpdirname:
                z.extract(name, tmpdirname)
                df = decode_blackbox(tmpdirname + "/" + name)

            name = name.replace(".TXT", "").split("/")[-1]
            parts = name.split("_")

            df.dropna(inplace=True, subset=["motor[0]"])
            df.rename(columns={"motor[0]": "throttle"}, inplace=True)
            df["motor"] = parts[0]
            df["prop"] = parts[1]
            df["airspeed"] = parts[2]
            df["cells"] = parts[3]
            df["battery"] = parts[4]
            df["run"] = parts[5]
            blackbox_dfs[name.lower()] = df

    # Create empty zip file
    with zipfile.ZipFile(OUTPUT_ZIP, "w") as z:
        pass

    common_dfs = set(thrust_dfs.keys()).intersection(set(blackbox_dfs.keys()))
    for name in common_dfs:
        print(name)
        df = blackbox_dfs[name][BLACKBOX_COLS].copy()
        metadata = blackbox_dfs[name][METADATA].iloc[0]
        bins = (
            df["throttle"]
            .index[(df["throttle"] - df["throttle"].shift(1)).apply(lambda x: x > 20)]
            .tolist()
        )
        df["throttle_group"] = pd.qcut(
            df["throttle"],
            q=[0] + [val / len(df["throttle"]) for val in bins] + [1],
            labels=list(map(str, bins)) + ["max"],
        )
        df = df.groupby("throttle_group").mean()
        df.reset_index(inplace=True)
        df.drop(columns=["throttle_group"], inplace=True)

        df_thrust = thrust_dfs[name][THRUST_COLS]
        df_thrust["thrust"] = -df_thrust["Drag"]

        df = df.join(df_thrust)
        df["percent_throttle"] = (
            (df["throttle"] - MIN_THROTTLE) / (MAX_THROTTLE - MIN_THROTTLE) * 100
        )
        for col in METADATA:
            df[col] = metadata[col]

        # Write to zip file
        with tempfile.NamedTemporaryFile() as tmp:
            df.to_csv(tmp.name, index=False)
            with zipfile.ZipFile(OUTPUT_ZIP, "a") as z:
                z.write(tmp.name, name + ".csv")


if __name__ == "__main__":
    main(sys.argv)
