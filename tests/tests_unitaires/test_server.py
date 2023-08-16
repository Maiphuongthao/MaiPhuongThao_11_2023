import pytest
import datetime
from tests.conftest import club1, club2, futureCompetition, client
from server import loadClubs, loadCompetitions, MAX_BOOKABLE_PLACES
# test if test json loaded

class TestData:
    def test_loadClubs(self):
        clubs = loadClubs("tests/clubs.json")
        expected = [
                {
        "name":"Test club 1",
        "email":"test1@test.com",
        "points":"11"
    },
    {
        "name":"Zero test club 0",
        "email": "test0@test.com",
        "points":"0"
    },
    {   "name":"Full test club 2",
        "email": "test2@test.com",
        "points":"100"
    }
        ]
        print(f"clubs = {clubs}")
        assert clubs == expected

    def test_loadCompetitions(self):
        competitions = loadCompetitions("tests/competitions.json")
        expected = [
        {
            "name": "Past competition",
            "date": datetime.datetime(2022, 3, 27, 10),
            'is_passed': True,
            "numberOfPlaces": "10"
        },
        {
            "name": "Future competition",
            "date": datetime.datetime(2024, 10, 22, 13, 30),
            'is_passed': False,
            "numberOfPlaces": "8"
        },
        {
            "name": "Future ahead competition",
            "date": datetime.datetime(2030, 10, 22, 13, 30),
            'is_passed': False,
            "numberOfPlaces": "50"
        }
    ]
        assert competitions == expected


        
#test endpoints with authentification not loggin & login
class TestAuthentification:

    @pytest.mark.parametrize("test_enpoint, expected_status", [
    ("/", 200),
    ("/showSummary", 405),
    ("/purchasePlaces", 405),
    ("/logout", 302),
    ("/points", 200)
    ])
    def test_endpoint(self, client, test_enpoint, expected_status):
        assert client.get(test_enpoint).status_code == expected_status
    
    def test_correct_email_redirect(self, client, club1):
        email = club1["email"]
        response = client.post('/showSummary', data={'email' : email}, follow_redirects=True)
        assert response.status_code == 200

    def test_incorrect_email_redirect(self, client):
        email = "unknownaddress@email.com"
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 302
        response_redirect = client.post('/showSummary', data={'email' : email}, follow_redirects=True)
        assert "Sorry, that email wasn&#39;t found." in response_redirect.data.decode('utf-8')

#test booking

class TestPurchase:
    def test_valid_booking(self, client, club1, futureCompetition):
        places = 1
        data = {"competition":futureCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        print(f"res ==== {data}")
        assert response.status_code == 200

    def test_valid_booking_update_club_points(self, client, club1, futureCompetition):
        places = 1
        clubs_points = int(club1["points"])
        data = {"competition":futureCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Points available: 10' in response.data.decode('utf-8')

    def test_not_enough_point_to_book(self, client, club2, futureCompetition):
        places = int(club2["points"]) + 1
        data = {"competition":futureCompetition['name'], "club":club2['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Try again - your points is less than what you book. ' in response.data.decode('utf-8')

    def test_shoudnt_book_more_than_max(self, client, club1, futureCompetition):
        places =  MAX_BOOKABLE_PLACES+ 1
        data = {"competition":futureCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Try again - You cannot book more than 12 places. ' in response.data.decode('utf-8')

    def test_shouldnt_book_past_competition(self, client, club1, pastCompetition):
        places =  1
        data = {"competition":pastCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Sorry- You can not book a passed competition.' in response.data.decode('utf-8')

#test display
class TestDisplay:
    def test_correct_display_points_board(self, client):
        clubs = loadClubs("tests/clubs.json")
        res = client.get('/points')
        assert res.status_code == 200
        for c in clubs:
            assert c["name"] in res.data.decode('utf-8')
            assert c["points"] in res.data.decode('utf-8')
