import zipfile
import pandas as pd


def decode_thrust(zip_path: str):
    run_dfs: dict[str, pd.DataFrame] = dict()
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for run in zip_ref.namelist():
            run_config_parts = run.split("_")
            motor = run_config_parts[0]
            prop = run_config_parts[1]
            battery = run_config_parts[2]
            run_name = run_config_parts[3]
            if run_name not in run_dfs:
                run_dfs[run_name] = pd.DataFrame(
                    columns=["motor", "prop", "battery", "avg_max_thrust (g)"]
                )

            lines = zip_ref.read(run).decode().replace("\r", "").split("\n\n")
            max_thrust = 0
            for line in lines:
                parts = line.split("\t")
                try:
                    if not parts[1][0].isdigit():  # ignore control logs
                        continue
                except:
                    continue
                timestamp = parts[0]
                datapoints = parts[1].split("\n")
                for datapoint in datapoints:
                    x, y = datapoint.split(",")
                    max_thrust = max(max_thrust, -float(y))

            run_dfs[run_name] = pd.concat(
                [
                    run_dfs[run_name],
                    pd.DataFrame.from_records(
                        [
                            {
                                "motor": motor,
                                "prop": prop,
                                "battery": battery,
                                "avg_max_thrust (g)": max_thrust,
                            }
                        ]
                    ),
                ],
                ignore_index=True,
            )

    return run_dfs
