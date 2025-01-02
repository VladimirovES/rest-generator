import subprocess
import sys
from typing import Optional

def run_command(command: str, cwd: Optional[str] = None) -> None:
    print(f"Running command: {command}")
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running command: {command}\nError: {e}")
        sys.exit(e.returncode)
    else:
        print("Command executed successfully.\n")
