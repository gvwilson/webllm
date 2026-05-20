import subprocess
import time
from pathlib import Path

import pytest

LESSON_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def server_url():
    proc = subprocess.Popen(
        ["uv", "run", "uvicorn", "server_pw:app", "--port", "8000"],
        cwd=LESSON_DIR,
    )
    time.sleep(1.5)
    yield "http://localhost:8000"
    proc.terminate()
    proc.wait()
