import os
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_DIR / ".venv" / "bin" / "python"


def ensure_venv_python() -> None:
    if Path(sys.prefix).resolve() != (PROJECT_DIR / ".venv").resolve():
        os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(__file__)])


def start_database() -> None:
    try:
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=PROJECT_DIR,
            check=True,
            stdout=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print("Fehler: Docker wurde nicht gefunden.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Fehler: MongoDB-Docker-Container konnte nicht gestartet werden.")
        sys.exit(1)


def main() -> None:
    ensure_venv_python()
    start_database()

    from book_exam_app import run

    run()


if __name__ == "__main__":
    main()
