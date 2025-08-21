from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from store.models import Collection, Product
from model_bakery import baker
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
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_valid_returns_400(self, create_collection, authenticate):
        authenticate(True)
        response = create_collection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_collection_is_created_returns_200(self, authenticate, create_collection):
        authenticate(True)
        response = create_collection({'title': 'a'} )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exist_returns_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

    def test_if_collection_updated_returns_200(self, api_client, authenticate):
        collection = baker.make(Collection)
        authenticate(True)
        response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'Arts'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Arts'

    def test_deleting_collection_contain_product_returns_405(self, api_client, authenticate):
        product = baker.make(Product)
        authenticate(True)

        response = api_client.delete(f'/store/collections/{product.collection.id}/')
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_deleting_collection_returns_200(self, api_client, authenticate):
        collection = baker.make(Collection)
        authenticate(True)

        response = api_client.delete(f'/store/collections/{collection.id}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT