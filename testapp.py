import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Renters, Rentals

# TEST CASE CLASS


class RoommateFinderTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = 'postgresql://ulxxdhwkddjwqy:85e70942145391f2ffdb063db6bcc4e425659cdef7682654893e88d2a2c945c2@ec2-18-209-78-11.compute-1.amazonaws.com:5432/d3u8jvplibk40e'
        LANDLORD_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTI4YTlhZTk1ZDc0YTM3NGQ0ZTQiLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTgyNjYsImV4cCI6MTY2NjM2NTQ2NiwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.vAdB2VGYFZRKhChyeWYJ5fGqC5BUgcQTjd2g54F15bk-m-Nl0Vd7Y-zXFfmry-RVJd4mj1qIue0h5IxwRcWgEAnguRZ_20vUDJmCVZmeT8XzsourYr4zVGH5h8Rq9xiEzyqKjudIDQIUGnU4cUTfsRx9sto_MujltR7_LtEBwGJPCTQRrpYb9MtVrzyE2PJARAuM_gukrtLYExAW3qP6NmRvn0mlMxnANgXBlPf88-UbomGEFNJ8BZjSD8frUieo06MO1cZzjuHcUMqupTQfeh8H4Aj-fx3Dx3YgRG0oxIHOj4ekCfPx-zssW83d0uoxVP-r4UdwT3Z0uPEFSGTtdg'
        TENANT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTJhZWExMjc1MmZmNDhmZDJkZTciLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTg0MDUsImV4cCI6MTY2NjM2NTYwNSwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.PJeN5hH6gdSYsWCYHfIE3bSTsUppPCvYRgwBni2bY4QuHgTzuMnH22iXE96ZEX5prJUoiiWYiqIe57MOla2TG-mtwxzctv2VxvErGmRHV6XHJ01PwcpdI0lc7n3EJ5shEuJobjU72TBEnuFT3hgOe3eeCLLuOTv8mMx8rgmOQMbdyhT1Xcco0LSgH-2hkhMATYbYeZOSwbOG2NGrBtUXz4NXO3QNDekRArjQufhZdbGl3i-TnySAAMu1dAokt-f627EGxg6JvtJyOeKUbXt6vNKqjn_YLSyT9WrsLkcvtczV8VS6zaaV6AMjIN3NB9EITsvLHKZ0oE17t3uVUlBLrA'
        ROOMMATE_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTJjZDlhZTk1ZDc0YTM3NGQ0ZTciLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTg1MzksImV4cCI6MTY2NjM2NTczOSwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.UVW2ySBneROsBj1Ub2m1OYPSLiBozBzKKpwS-A6-z9PUyzZih69aPZ1cZI8ftsehttHgMS-mej8h8Vh48v9Kp0njhOVJIq5VhXCy1bYS0jMKTlCtzK4BrQ0q49IeFIMpBZCaiFJHJQlyfgscFtNlTLPXNztHRdNbAco2W-8fYdaoBaTgVzLQXj8cQfS8w6bXg-iJew93__yFmCoG9TLGnfuBgLPa9z4YmveY7Lcwm2x6IR_Fa2c7qjy1m5CJ9E0Aoo34c878hyrvd8feVYQaYrAA-CLMvPu6Bx4YkxqVujO5DimvJGRmAbQc8OjfqF0TK1-6pQ6gOeHopE6ZRXo_bQ'

        self.landlord_auth_header = {'Authorization':
                                      'Bearer ' + LANDLORD_TOKEN}
        self.tenant_auth_header = {'Authorization':
                                     'Bearer ' + TENANT_TOKEN}
        self.roommate_auth_header = {'Authorization':
                                     'Bearer ' + ROOMMATE_TOKEN}
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)


# Test data set-up for all tests down under

        self.post_Renter = {
            'name': "Michael",
            'age': 45,
            'gender': 'MALE'
        }

        self.post_Renter1 = {
            'name': "George",
            'age': 28,
            'gender': 'MALE'
        }

        self.post_Renter2 = {
            'name': "Markus",
            'age': 39,
            'gender': 'MALE'
        }

        self.post_Renter_name_missing = {
            'age': 34,
            'gender': "MALE"
        }

        self.post_Renter_gender_missing = {
            'age': 34,
            'name': "John"
        }

        self.patch_Renter_on_age = {
            'age': 55
        }

        self.post_Rental = {
            'address': "SAMPLE Rental",
            'rent': "200"
        }

        self.post_Rental1 = {
            'address': "MAHABHARATA",
            'rent': "300"
        }

        self.post_Rental2 = {
            'address': "MAHABHARATA - 2",
            'rent': "2000"
        }

        self.post_Rental_address_missing = {
            'rent': "2030"
        }

        self.post_Rental_rent_missing = {
            'address': "RAMAYANA"
        }

        self.patch_Rental_on_rent = {
            'rent': "3000"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass


# Test cases for the Endpoints related to /Renters
# ------------------------------------------------
# GET Positive case - Landlord Role


    def test_get_Renters1(self):
        res = self.client().get('/Renters?page=1',
                                headers=self.landlord_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['Renters']) > 0)

# GET Positive case - Tenant Role
    def test_get_Renters2(self):
        res = self.client().get('/Renters?page=1',
                                headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['Renters']) > 0)

# GET Positive case - Roommate Role
    def test_get_Renters3(self):
        res = self.client().get('/Renters?page=1',
                                headers=self.roommate_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['Renters']) > 0)

# POST Positive case - Tenant Role
    def test_post_new_Renter1(self):
        res = self.client().post('/Renters',
                                 json=self.post_Renter1,
                                 headers=self.tenant_auth_header)
        data = json.loads(res.data)

        Renter = Renters.query.filter_by(id=data['Renter-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(Renter)

# POST Positive case - Roommate Role
    def test_post_new_Renter2(self):
        res = self.client().post('/Renters',
                                 json=self.post_Renter2,
                                 headers=self.roommate_auth_header)
        data = json.loads(res.data)

        Renter = Renters.query.filter_by(id=data['Renter-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(Renter)

# POST Negative Case - Add Renter with missing name
# - Tenant Role
    def test_post_new_Renter_name_missing(self):
        res = self.client().post('/Renters',
                                 json=self.post_Renter_name_missing,
                                 headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add Renter with missing gender - Tenant Role
    def test_post_new_Renter_gender_missing(self):
        res = self.client().post('/Renters',
                                 json=self.post_Renter_gender_missing,
                                 headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing Renter - Tenant Role
    def test_delete_Renter(self):
        res = self.client().post('/Renters', json=self.post_Renter,
                                 headers=self.tenant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        Renter_id = data['Renter-added']

        res = self.client().delete('/Renters/{}'.format(Renter_id),
                                   headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['Renter-deleted'], Renter_id)

# DELETE Negative Case Renter not found - Tenant Role
    def test_delete_Renter_not_found(self):
        res = self.client().delete('/Renters/999',
                                   headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update age of an existing
# Renter - Tenant Role
    def test_patch_Renter(self):
        res = self.client().patch('/Renters/2',
                                  json=self.patch_Renter_on_age,
                                  headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['Renter-updated'], 2)

# PATCH Negative case - Update age for non-existent Renter
# - Tenant Role
    def test_patch_Renter_not_found(self):
        res = self.client().patch('/Renters/99',
                                  json=self.patch_Renter_on_age,
                                  headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# RBAC - Test Cases:
# RBAC GET Renters w/o Authorization header
    def test_get_Renters_no_auth(self):
        res = self.client().get('/Renters?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Authorization header is expected.')

# RBAC POST Renters with wrong Authorization header - Landlord Role
    def test_post_Renter_wrong_auth(self):
        res = self.client().post('/Renters',
                                 json=self.post_Renter1,
                                 headers=self.landlord_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

# RBAC DELETE Negative Case - Delete an existing Renter
# without appropriate permission
    def test_delete_Renter_wrong_auth(self):
        res = self.client().delete('/Renters/10',
                                   headers=self.landlord_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')


# Test cases for the Endpoints related to /Rentals
# ------------------------------------------------
# GET Positive case - Landlord Role


    def test_get_Rentals1(self):
        res = self.client().get('/Rentals?page=1',
                                headers=self.landlord_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['Rentals']) > 0)

# GET Positive case - Tenant Role
    def test_get_Rentals2(self):
        res = self.client().get('/Rentals?page=1',
                                headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['Rentals']) > 0)

# GET Positive case - Roommate Role
    def test_get_Rentals3(self):
        res = self.client().get('/Rentals?page=1',
                                headers=self.roommate_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['Rentals']) > 0)

# POST Positive case - Roommate Role
    def test_post_new_Rental2(self):
        res = self.client().post('/Rentals', json=self.post_Rental2,
                                 headers=self.roommate_auth_header)
        data = json.loads(res.data)

        Rental = Rentals.query.filter_by(id=data['Rental-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(Rental)

# POST Negative Case - Add Rental with missing address
# - Roommate Role
    def test_post_new_Rental_address_missing(self):
        res = self.client().post('/Rentals',
                                 json=self.post_Rental_address_missing,
                                 headers=self.roommate_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add Rental with missing release date
# - Roommate Role
    def test_post_new_Rental_rent_missing(self):
        res = self.client().post('/Rentals',
                                 json=self.post_Rental_rent_missing,
                                 headers=self.roommate_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing Rental - Roommate Role
    def test_delete_Rental(self):
        res = self.client().post('/Rentals',
                                 json=self.post_Rental,
                                 headers=self.roommate_auth_header)
        data = json.loads(res.data)

        Rental_id = data['Rental-added']

        res = self.client().delete('/Rentals/{}'.format(Rental_id),
                                   headers=self.roommate_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['Rental-deleted'], Rental_id)

# DELETE Negative Case Rental not found - Roommate Role
    def test_delete_Rental_not_found(self):
        res = self.client().delete('/Rentals/777',
                                   headers=self.roommate_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update Release Date of
# an existing Rental - Tenant Role
    def test_patch_Rental(self):
        res = self.client().patch('/Rentals/2',
                                  json=self.patch_Rental_on_rent,
                                  headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['Rental-updated'], 2)

# PATCH Negative case - Update Release Date for
# non-existent Rental - Tenant Role
    def test_patch_Rental_not_found(self):
        res = self.client().patch('/Rentals/99',
                                  json=self.patch_Rental_on_rent,
                                  headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# RBAC - Test Cases:
# RBAC GET Rentals w/o Authorization header
    def test_get_Rentals_no_auth(self):
        res = self.client().get('/Rentals?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'authorization_header_missing')

# RBAC POST Rentals with wrong Authorization header - Tenant Role
    def test_post_Rental_wrong_auth(self):
        res = self.client().post('/Rentals', json=self.post_Rental1,
                                 headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

# RBAC DELETE Negative Case - Delete an existing Rental
# without appropriate permission
    def test_delete_Rental_wrong_auth(self):
        res = self.client().delete('/Rentals/8',
                                   headers=self.tenant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')


# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()