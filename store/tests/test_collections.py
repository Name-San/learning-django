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