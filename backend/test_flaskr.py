import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
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
        self.assertEqual(len(data['questions']), 10)
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

    def test_page_doesnt_exist(self):
        """Make sure we get a 404 error on a page which we know doesn't exist"""
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  # Now using API-friendly custom error handlers
        self.assertEqual(data['error'], 404)


    def test_delete_question(self):
        """Create a new question, then test deleting it"""
        
        # Create a test question to delete
        new_question = Question(question='A resurgent nuclear technology called LFTR, thought by many capable of \
            meeting all global energy needs, is based on what element?', answer="Thorium", category="1", difficulty=4)
        new_question.insert()
        nq_id = new_question.id

        # Test added successfully
        all_questions = Question.query.all()
        self.assertEqual(len(all_questions), 20)    # 19 originally in test DB

        # Delete it through route
        res = self.client().delete(f'/api/questions/{nq_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], nq_id)

    def test_invalid_delete_question(self):
        """Try to delete a question that doesn't exist, should get a 404 error"""
        res = self.client().delete(f'/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()