import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

# TEST CASE CLASS


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = 'postgres://ulxxdhwkddjwqy:85e70942145391f2ffdb063db6bcc4e425659cdef7682654893e88d2a2c945c2@ec2-18-209-78-11.compute-1.amazonaws.com:5432/d3u8jvplibk40e'
        #Landlord
        ASSISTANT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTI4YTlhZTk1ZDc0YTM3NGQ0ZTQiLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTgyNjYsImV4cCI6MTY2NjM2NTQ2NiwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.vAdB2VGYFZRKhChyeWYJ5fGqC5BUgcQTjd2g54F15bk-m-Nl0Vd7Y-zXFfmry-RVJd4mj1qIue0h5IxwRcWgEAnguRZ_20vUDJmCVZmeT8XzsourYr4zVGH5h8Rq9xiEzyqKjudIDQIUGnU4cUTfsRx9sto_MujltR7_LtEBwGJPCTQRrpYb9MtVrzyE2PJARAuM_gukrtLYExAW3qP6NmRvn0mlMxnANgXBlPf88-UbomGEFNJ8BZjSD8frUieo06MO1cZzjuHcUMqupTQfeh8H4Aj-fx3Dx3YgRG0oxIHOj4ekCfPx-zssW83d0uoxVP-r4UdwT3Z0uPEFSGTtdg'
        #Tenant
        DIRECTOR_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTJhZWExMjc1MmZmNDhmZDJkZTciLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTg0MDUsImV4cCI6MTY2NjM2NTYwNSwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.PJeN5hH6gdSYsWCYHfIE3bSTsUppPCvYRgwBni2bY4QuHgTzuMnH22iXE96ZEX5prJUoiiWYiqIe57MOla2TG-mtwxzctv2VxvErGmRHV6XHJ01PwcpdI0lc7n3EJ5shEuJobjU72TBEnuFT3hgOe3eeCLLuOTv8mMx8rgmOQMbdyhT1Xcco0LSgH-2hkhMATYbYeZOSwbOG2NGrBtUXz4NXO3QNDekRArjQufhZdbGl3i-TnySAAMu1dAokt-f627EGxg6JvtJyOeKUbXt6vNKqjn_YLSyT9WrsLkcvtczV8VS6zaaV6AMjIN3NB9EITsvLHKZ0oE17t3uVUlBLrA'
        #Roommate
        PRODUCER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTJjZDlhZTk1ZDc0YTM3NGQ0ZTciLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTg1MzksImV4cCI6MTY2NjM2NTczOSwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.UVW2ySBneROsBj1Ub2m1OYPSLiBozBzKKpwS-A6-z9PUyzZih69aPZ1cZI8ftsehttHgMS-mej8h8Vh48v9Kp0njhOVJIq5VhXCy1bYS0jMKTlCtzK4BrQ0q49IeFIMpBZCaiFJHJQlyfgscFtNlTLPXNztHRdNbAco2W-8fYdaoBaTgVzLQXj8cQfS8w6bXg-iJew93__yFmCoG9TLGnfuBgLPa9z4YmveY7Lcwm2x6IR_Fa2c7qjy1m5CJ9E0Aoo34c878hyrvd8feVYQaYrAA-CLMvPu6Bx4YkxqVujO5DimvJGRmAbQc8OjfqF0TK1-6pQ6gOeHopE6ZRXo_bQ'

        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + PRODUCER_TOKEN}
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)


# Test data set-up for all tests down under

        self.post_actor = {
            'name': "Michael",
            'age': 45,
            'gender': 'MALE'
        }

        self.post_actor1 = {
            'name': "George",
            'age': 28,
            'gender': 'MALE'
        }

        self.post_actor2 = {
            'name': "Markus",
            'age': 39,
            'gender': 'MALE'
        }

        self.post_actor_name_missing = {
            'age': 34,
            'gender': "MALE"
        }

        self.post_actor_gender_missing = {
            'age': 34,
            'name': "John"
        }

        self.patch_actor_on_age = {
            'age': 55
        }

        self.post_movie = {
            'title': "SAMPLE MOVIE",
            'release_date': "2090-10-10"
        }

        self.post_movie1 = {
            'title': "MAHABHARATA",
            'release_date': "2030-10-10"
        }

        self.post_movie2 = {
            'title': "MAHABHARATA - 2",
            'release_date': "2032-10-10"
        }

        self.post_movie_title_missing = {
            'release_date': "2030-10-10"
        }

        self.post_movie_reldate_missing = {
            'title': "RAMAYANA"
        }

        self.patch_movie_on_reldate = {
            'release_date': "2035-10-10"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass


# Test cases for the Endpoints related to /actors
# ------------------------------------------------
# GET Positive case - Assistant Role


    def test_get_actors1(self):
        res = self.client().get('/actors?page=1',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# GET Positive case - Director Role
    def test_get_actors2(self):
        res = self.client().get('/actors?page=1',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# GET Positive case - Producer Role
    def test_get_actors3(self):
        res = self.client().get('/actors?page=1',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# POST Positive case - Director Role
    def test_post_new_actor1(self):
        res = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Positive case - Producer Role
    def test_post_new_actor2(self):
        res = self.client().post('/actors',
                                 json=self.post_actor2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Negative Case - Add actor with missing name
# - Director Role
    def test_post_new_actor_name_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_name_missing,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add actor with missing gender - Director Role
    def test_post_new_actor_gender_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_gender_missing,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing actor - Director Role
    def test_delete_actor(self):
        res = self.client().post('/actors', json=self.post_actor,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['actor-added']

        res = self.client().delete('/actors/{}'.format(actor_id),
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-deleted'], actor_id)

# DELETE Negative Case actor not found - Director Role
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/999',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update age of an existing
# actor - Director Role
    def test_patch_actor(self):
        res = self.client().patch('/actors/2',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-updated'], 2)

# PATCH Negative case - Update age for non-existent actor
# - Director Role
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/99',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# RBAC - Test Cases:
# RBAC GET actors w/o Authorization header
    def test_get_actors_no_auth(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Authorization header is expected.')

# RBAC POST actors with wrong Authorization header - Assistant Role
    def test_post_actor_wrong_auth(self):
        res = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

# RBAC DELETE Negative Case - Delete an existing actor
# without appropriate permission
    def test_delete_actor_wrong_auth(self):
        res = self.client().delete('/actors/10',
                                   headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')


# Test cases for the Endpoints related to /movies
# ------------------------------------------------
# GET Positive case - Assistant Role


    def test_get_movies1(self):
        res = self.client().get('/movies?page=1',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Positive case - Director Role
    def test_get_movies2(self):
        res = self.client().get('/movies?page=1',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Positive case - Producer Role
    def test_get_movies3(self):
        res = self.client().get('/movies?page=1',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# POST Positive case - Producer Role
    def test_post_new_movie2(self):
        res = self.client().post('/movies', json=self.post_movie2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie = Movies.query.filter_by(id=data['movie-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

# POST Negative Case - Add movie with missing title
# - Producer Role
    def test_post_new_movie_title_missing(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_title_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add movie with missing release date
# - Producer Role
    def test_post_new_movie_reldate_missing(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_reldate_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing movie - Producer Role
    def test_delete_movie(self):
        res = self.client().post('/movies',
                                 json=self.post_movie,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie_id = data['movie-added']

        res = self.client().delete('/movies/{}'.format(movie_id),
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-deleted'], movie_id)

# DELETE Negative Case movie not found - Producer Role
    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/777',
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update Release Date of
# an existing movie - Director Role
    def test_patch_movie(self):
        res = self.client().patch('/movies/2',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-updated'], 2)

# PATCH Negative case - Update Release Date for
# non-existent movie - Director Role
    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/99',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# RBAC - Test Cases:
# RBAC GET movies w/o Authorization header
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'authorization_header_missing')

# RBAC POST movies with wrong Authorization header - Director Role
    def test_post_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.post_movie1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

# RBAC DELETE Negative Case - Delete an existing movie
# without appropriate permission
    def test_delete_movie_wrong_auth(self):
        res = self.client().delete('/movies/8',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')


# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()