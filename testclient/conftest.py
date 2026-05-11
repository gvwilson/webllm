import subprocess
import time
from pathlib import Path

import pytest

LESSON_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def server_url():
    proc = subprocess.Popen(
        ["uv", "run", "litestar", "run", "--app", "server_pw:app"],
        cwd=LESSON_DIR,
    )
    time.sleep(1.5)
    yield "http://localhost:8000"
    proc.terminate()
    proc.wait()
