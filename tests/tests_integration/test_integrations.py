from server import MAX_BOOKABLE_PLACES

class TestIntegration:
    def test_booking_senario(self, client,club1, futureCompetition, pastCompetition):

        assert client.get('/').status_code==200
        email = {'email': club1['email']}
        res =  client.post('/showSummary', data=email)
        assert res.status_code==200

        page = client.get(f"book/{futureCompetition['name']}/{club1['name']}")
        assert page.status_code==200

        places = 1
        data = {"competition":futureCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Points available: 9' in response.data.decode('utf-8')

        page = client.get(f"book/{pastCompetition['name']}/{club1['name']}")
        assert page.status_code==200

        places =  MAX_BOOKABLE_PLACES + 1
        data = {"competition":futureCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Try again - You cannot book more than 12 places. ' in response.data.decode('utf-8')

        places = int(club1["points"]) + 1
        data = {"competition":futureCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Try again - your points is less than what you book. ' in response.data.decode('utf-8')

        places =  1
        data = {"competition":pastCompetition['name'], "club":club1['name'], "places":places}
        response = client.post('/purchasePlaces', data = data)
        assert response.status_code == 200
        assert 'Sorry- You can not book a passed competition.' in response.data.decode('utf-8')

        logout= client.get('/logout')
        assert logout.status_code==302

        page=client.get('/points')
        assert page.status_code == 200
