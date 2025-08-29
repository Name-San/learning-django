from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from store.models import Collection, Product, Review
from model_bakery import baker
import pytest



@pytest.fixture
def create_collection(api_client):
    def do_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_collection

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product


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

@pytest.mark.django_db
class TestProducts:
    def test_if_anonymous_returns_401(self, authenticate, create_product):
        response = create_product({'title': "Sample Product", "unit_price": 3, "inventory": 11, 'collection': 2})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_unauthenticated_user_returns_403(self, create_collection, authenticate):
        authenticate()
        response = create_collection({'title': 'Bumble Bee'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authenticated_user_returns_200(self, authenticate, api_client):
        authenticate(True)
        response = api_client.get('/store/products/', {'title':'Transformer', 'unit_price': 1})
        assert response.status_code == status.HTTP_200_OK

    def test_if_invalid_product_returns_400(self, authenticate, create_product):
        authenticate(True)
        response = create_product({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exist_returns_200(self, api_client):
        product = baker.make(Product)
        response = api_client.get(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_if_product_updated_returns_200(self, api_client, authenticate):
        product = baker.make(Product)
        authenticate(True)
        response = api_client.put(f'/store/products/{product.id}/', 
                                  {
                                    "title": "Gundam",
                                    "slug": "gundam",
                                    "description": "Gundam figurine",
                                    "unit_price": 4.0,
                                    "inventory": 1,
                                    "collection": 1,
                                })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Gundam'
    
    def test_if_product_deleted_returns_204(self, api_client, authenticate):
        product = baker.make(Product)
        authenticate(True)
        response = api_client.delete(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
class TestReviews:
    def test_if_can_add_reviews_returns_200(self, api_client):
        product = baker.make(Product)
        response = api_client.post(f'/store/products/{product.id}/reviews/', {"name": 'Anna', "description": 'This is Anna.'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Anna'

    def test_update_review_returns_200(self, api_client):
        review = baker.make(Review)
        response = api_client.patch(f'/store/products/{review.product.id}/reviews/{review.id}/', {"name": "Anna"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Anna'

    def test_delete_review_returns_204(self, api_client):
        review = baker.make(Review)
        response = api_client.delete(f'/store/products/{review.product.id}/reviews/{review.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT