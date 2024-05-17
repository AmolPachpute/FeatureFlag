
from rest_framework import status
from rest_framework.test import APITestCase


class FeatureFlagTests(APITestCase):

    host = "http://127.0.0.1:8000/api"

    def initialize_database(self, **data):
        """
        Initialize database with one record. data can be custom or default data will be added if not passed
        """
        url = self.host + "/flags/"
        if not data:
            data = {
                "id": "feature15",
                "description": "test feature",
                "is_enabled": "true"
            }
        response = self.client.post(url, data, format='json')

    def test_post(self):
        """
        Test post endpoint
        """
        url = self.host + "/flags/"
        data = {
                "id": "feature14",
                "description": "test feature",
                "is_enabled": "true"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch(self):
        """
        Test patch endpoint
        """

        self.initialize_database()
        url = self.host + "/flags/feature15/"
        data = {
                "description": "Unit test patch feature 15",
                "is_enabled": "false"
                }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all(self):
        """
        Test GET all records.
        """
        self.initialize_database()
        data = {
            "id": "feature16",
            "description": "test feature16",
            "is_enabled": "false"
        }
        self.initialize_database(**data)
        url = self.host + "/flags/"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single(self):
        """
        Test GET only one record
        """
        self.initialize_database()
        url = self.host + "/flags/feature15/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("id" in response.data)

    def test_disable_feature(self):
        """
        Disable a feature flag which was initially enabled
        """
        self.initialize_database()
        url = self.host + "/flags/feature15/"
        data = {
            "is_enabled": "false"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = self.host + "/flags/"
        response = self.client.get(url, format='json')
        self.assertFalse(response.data[0].get("is_enabled"))
        self.assertEqual(len(response.data), 1)

    def test_enable_feature(self):
        """
        Enable a feature flag
        """
        self.initialize_database()
        url = self.host + "/flags/feature15/"
        data = {
            "is_enabled": "false"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get("is_enabled"))

        data = {
            "is_enabled": "true"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("is_enabled"))



