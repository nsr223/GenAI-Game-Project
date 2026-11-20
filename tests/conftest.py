from pathlib import Path

import pytest

from game.content import load_content

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def content():
    return load_content(REPO_ROOT / "data")
