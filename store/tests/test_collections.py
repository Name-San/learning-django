from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.fixture
def create_collection(api_client):
    def do_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_collection

@pytest.mark.django_db
class TestCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
        authenticate()        
        response = create_collection({'title': 'a'})
        assert response.status_code != status.HTTP_403_FORBIDDEN

    def test_if_data_is_valid_returns_400(self, create_collection, authenticate):
        authenticate(True)
        response = create_collection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_collection_is_created_returns_200(self, authenticate, create_collection):
        authenticate(True)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0