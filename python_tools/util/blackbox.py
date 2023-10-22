import pandas as pd
import platform
import os
import tempfile


def decode_blackbox(log_path: str):
    """
    Decode the blackbox data from the path
    """
    assert os.path.isfile(log_path), "File does not exist (might be a directory)"
    operating_system = platform.system()
    log_path = os.path.abspath(log_path)
    old_wd = os.getcwd()
    try:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        with tempfile.NamedTemporaryFile("w+", suffix=".csv") as tempf:
            if operating_system == "Windows":
                os.system(
                    '../libs/blackbox-tools-6.0.0_win64/blackbox_decode.exe "'
                    + log_path
                    + '" --stdout > '
                    + tempf.name,
                )
            elif operating_system == "Darwin":  # Mac
                os.system(
                    '../libs/blackbox-tools-6.0.0_macos/blackbox_decode "'
                    + log_path
                    + '" --stdout > '
                    + tempf.name,
                )
            elif operating_system == "Linux":
                os.system(
                    '../libs/blackbox-tools-6.0.0_linux/blackbox_decode "'
                    + log_path
                    + '" --stdout > '
                    + tempf.name,
                )
            else:
                raise Exception(
                    "Unknown operating system. Please use Windows, Mac, or Linux."
                )
            df = pd.read_csv(tempf.name)
            print(df.head())
        return df
    finally:
        os.chdir(old_wd)
