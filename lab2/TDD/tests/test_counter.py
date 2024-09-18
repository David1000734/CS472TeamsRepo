"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import pytest

# import unit under test - counter
from src.counter import app

# import file containing the status codes
from src import status

# Neccessary to change datatype from byte into dictionary
import ast

@pytest.fixture()
def client():
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED

        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        # Create a new counter
        result = client.post('/counters/count')
        assert result.status_code == status.HTTP_201_CREATED

        # Value returned by the endpoint is a byte. We must parse this into
        # a dictionary and attempt to retrieve usable data from it
        # ast will do this conversion into a dicitonary and then 
        # grab the only key in it for the value
        count = ast.literal_eval(result.data.decode('UTF-8'))['count']

        # Check for OK code from post
        result = client.put('/counters/count')
        assert result.status_code == status.HTTP_200_OK

        # Ensure the value was incremented from before
        result = ast.literal_eval(result.data.decode('UTF-8'))
        assert count + 1 == result['count']

        # Assert on attempting to update non-existing counters
        result = client.put('/counters/unknownCounter')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_counter(self, client):
        result = client.get('/counters/unKnownCounter')
        assert result.status_code == status.HTTP_404_NOT_FOUND

        result = client.get('/counters/count')
        assert result.status_code == status.HTTP_200_OK

        # This one must be 1 because it was incremented previously
        content = ast.literal_eval(result.data.decode('UTF-8'))
        assert 1 == content['count']
