import pandas as pd

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
from python_tools.util.blackbox import decode_blackbox

USAGE = "Usage: `python parse_windtunnel_data.py <log_path> <wind_tunnel_csv>:<test_point> [output_path]`"
HELP_MESSAGE = f"""
    This script combines the blackbox data with the wind tunnel data. It crops out the incompatible data.

    {USAGE}
        log_path: Path to the blackbox log
        wind_tunnel_csv: Path to the wind tunnel csv file
        test_point: The test point (TP) in the wind tunnel csv file
        output_path: Path to the output csv file (default: <log_path>_<wind_tunnel_csv>.csv)
""".strip()


def get_on_interval(df: pd.DataFrame):
    return df[df["rcData[3]"] == df["rcData[3]"].max()]


def main(args):
    if len(args) < 3 or args[1] == "-h" or args[1] == "--help":
        print(HELP_MESSAGE)
        return
    assert (
        len(args) <= 4
    ), f"Use quotes around file paths with spaces. Try `python parse_data.py --help`. {USAGE}"
    log_path = args[1]
    wind_tunnel_path = args[2].split(":")[0]
    test_point = args[2].split(":")[1]
    output_path = (
        args[3]
        if len(args) > 3
        else log_path[:-4] + "_" + wind_tunnel_path[:-4] + ".csv"
    )

    df_log = decode_blackbox(log_path)
    df_log = get_on_interval(df_log)
    df_log = df_log[
        ["time (us)", "vbat (V)", "amperage (A)", "rcData[3]", "motor[0]", "escRPM"]
    ]
    df_log.columns = ["time (us)", "vbat", "amperage", "throttle", "motor", "rpm"]
    df_log["Power (W)"] = df_log["vbat"] * df_log["amperage"]

    df_wind_tunnel = pd.read_csv(wind_tunnel_path)
    wind_tunnel_datapoint = df_wind_tunnel[
        df_wind_tunnel["TP"] == int(test_point)
    ].iloc[0]

    df_log["Thrust (lb)"] = -wind_tunnel_datapoint["Drag"]
    df_log["Lift"] = wind_tunnel_datapoint["Lift"]
    df_log["DYNAMIC PRESSURE"] = wind_tunnel_datapoint["DYNAMIC PRESSURE"]

    df_log.to_csv(output_path, index=False)


if __name__ == "__main__":
    main(sys.argv)
