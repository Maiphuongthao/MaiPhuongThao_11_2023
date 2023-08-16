import pytest
import server
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client(monkeypatch, clubs, competitions):
    monkeypatch.setattr(server, 'clubs', clubs)
    monkeypatch.setattr(server, 'competitions', competitions)
    with app.test_client() as client:
        yield client

@pytest.fixture
def club1():
    return loadClubs("tests/clubs.json")[0]

@pytest.fixture
def club2():
    return loadClubs("tests/clubs.json")[1]

@pytest.fixture
def clubs():
    return loadClubs("tests/clubs.json")

@pytest.fixture
def competitions():
    return loadCompetitions("tests/competitions.json")

@pytest.fixture
def futureCompetition():
    return loadCompetitions("tests/competitions.json")[1]

@pytest.fixture
def pastCompetition():
    return loadCompetitions("tests/competitions.json")[0]