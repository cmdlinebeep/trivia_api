import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:a@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """Gets the /api/categories endpoint and checks valid results"""
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        # print(res)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    def test_get_all_questions(self):
        """Gets all questions, including paginations (every 10 questions).  This endpoint should 
        return a list of questions, number of total questions, current category, categories."""
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        # This endpoint should default to page one, which should have id 5 first
        # and total questions of 19
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(data['questions'][0]['id'], 5)

    def test_pagination(self):
        """Tests the pagination by getting page 2 and looking for known features"""
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)

        # This endpoint should default to page one, which should have id 5 first
        # and total questions of 19
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 9)     # Should be 9 left
        self.assertEqual(data['questions'][0]['id'], 15)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()