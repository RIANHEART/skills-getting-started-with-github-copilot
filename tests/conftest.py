from fastapi.testclient import TestClient
from src.app import app, activities
import copy
import pytest


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the in-memory `activities` between tests."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
