from copy import deepcopy
from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.activities_store import activities


@pytest.fixture(autouse=True)
def reset_activities_store():
    """Restore the in-memory store after each test for isolation."""
    original_data = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_data)
