import pandas as pd
import platform
import os


def decode_blackbox(log_path: str):
    """
    Decode the blackbox data from the path
    """
    operating_system = platform.system()
    if operating_system == "Windows":
        os.system(
            "../libs/blackbox-tools-6.0.0_win64/blackbox_decode.exe "
            + log_path
            + " --limits"
        )
    elif operating_system == "Darwin":  # Mac
        os.system(
            "../libs/blackbox-tools-6.0.0_macos/blackbox_decode "
            + log_path
            + " --limits"
        )
    else:
        raise Exception("Unknown operating system. Please use Windows or Mac.")
    return pd.read_csv(log_path[:-4] + ".01.csv")
