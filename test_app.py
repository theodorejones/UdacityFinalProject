import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "example"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.producer_headers = {
            "Content-Type": "application/json",
            "Authorization":  os.environ.get('EXECUTIVE_PRODUCER')
        }
        self.assistant_headers = {
            "Content-Type": "application/json",
            "Authorization":  os.environ.get('CASTING_ASSISTANT')
        }

        self.new_renter = {
            'name': 'theodore',
            'age': 24,
            'gender': 'male'
        }
        self.new_rental = {
            'title': 'Avengers4'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_renters(self):
        res = self.client().get(
            '/renters', headers={"Authorization": "Bearer {}".
                                format(self.producer_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["renters"]))

    def test_401_get_renters_error(self):
        res = self.client().get('/renters')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    def test_get_all_rentals(self):
        res = self.client().get(
            '/rentals', headers={"Authorization": "Bearer {}".
                                format(self.producer_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["rentals"]))

    def test_401_get_rentals_error(self):
        res = self.client().get('/rentals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    def test_create_new_renter(self):
        res = self.client().post('/renters', json=self.new_renter,
                                 headers={"Authorization": "Bearer {}".
                                          format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['renters']))

    def test_401_create_new_renter(self):
        res = self.client().post('/renters', json=self.new_renter)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    def test_create_new_rental(self):
        res = self.client().post('/rentals', json=self.new_rental,
                                 headers={"Authorization": "Bearer {}".
                                          format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['rentals']))

    def test_401_create_new_rental(self):
        res = self.client().post('/rentals', json=self.new_rental)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    def test_update_renter(self):
        self.client().post('/renters', json=self.new_renter,
                           headers=self.producer_headers)
        res = self.client().patch('/renters/4', json={'name': 'ahmed',
                                                     'age': 25,
                                                     'gender': 'male'},
                                  headers={"Authorization": "Bearer {}".
                                           format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['renters']))

    def test_404_update_renter(self):
        res = self.client().patch('/renters/100', json={'name': 'ahmed',
                                                       'age': 25,
                                                       'gender': 'male'},
                                  headers={"Authorization": "Bearer {}".
                                           format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['renters']))

    def test_update_rental(self):
        self.client().post('/rentals', json=self.new_rental,
                           headers=self.producer_headers)
        res = self.client().patch(
            '/rentals/5', json={'title': 'Avenger2'},
            headers={"Authorization": "Bearer {}".
                     format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['rentals']))

    def test_404_update_rental(self):
        res = self.client().patch(
            '/rentals/100', json={'title': 'X-Men'},
            headers={"Authorization": "Bearer {}".
                     format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['rentals']))

    def test_delete_renter(self):
        self.client().post('/renters', json=self.new_renter,
                           headers=self.producer_headers)
        self.client().post('/renters', json=self.new_renter,
                           headers=self.producer_headers)
        res = self.client().delete('/renters/2',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['renters']))

    def test_404_delete_renter(self):
        res = self.client().delete('/renters/50',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['renters']))

    def test_delete_rental(self):
        self.client().post('/rentals', json=self.new_renter,
                           headers=self.producer_headers)
        self.client().post('/rentals', json=self.new_renter,
                           headers=self.producer_headers)
        res = self.client().delete('/rentals/2',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['rentals']))

    def test_404_delete_rental(self):
        res = self.client().delete('/rentals/50',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['rentals']))

    def test_get_all_renters_assistant(self):
        res = self.client().get(
            '/renters', headers={"Authorization": "Bearer {}".
                                format(self.assistant_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["renters"]))

    def test_401_get_renters_error_assistant(self):
        res = self.client().get('/renters')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    def test_get_all_rentals_assistant(self):
        res = self.client().get(
            '/rentals', headers={"Authorization": "Bearer {}".
                                format(self.assistant_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["rentals"]))

    def test_401_get_rentals_error_assistant(self):
        res = self.client().get('/rentals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")
        
if __name__ == "__main__":
  unittest.main()