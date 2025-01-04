import subprocess
import sys
from typing import Optional


def run_command(command: str, cwd: Optional[str] = None) -> None:
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
