from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db #Give access to database
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):

        client = APIClient()
        response = client.post('/store/collections/', {'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Testing User
    def test_if_user_is_not_admin_returns_403(self):
        
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post('/store/collections/', {'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):

        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    @pytest.mark.skip
    def test_if_data_is_valid_returns_201(self):

        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


