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

        # new question for testing
        self.new_question = {
            "question": "How many points is a touchdown worth?",
            "answer": "6",
            "category": "6",
            "difficulty": 1
            }

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
        new_question = Question(question=self.new_question['question'], answer=self.new_question['answer'], \
            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
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

    def test_post_new_question(self):
        """POST a new question and make sure it's in there on the last page"""
        # Count first and before doing any changes
        all_questions = Question.query.all()
        orig_num_questions = len(all_questions)
        self.assertEqual(orig_num_questions, 19)    # 19 originally in test DB

        # POST a new question using API endpoint
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)
        nq_id = data['added']

        self.assertEqual(data['success'], True)
        
        # The API returns the primary key id of the new question, but this changes with 
        # each test run as the DB keeps incrementing the sequence, so don't have a constant
        # value to check it against.
        # e.g. self.assertEqual(data['added'], ???)
        
        # Count that a new question was added, should have 20 after add
        all_questions = Question.query.all()
        self.assertEqual(len(all_questions), orig_num_questions + 1)    # 19 originally in test DB

        # Delete question from database again with another client request.  
        # API returns the primary key
        res = self.client().delete(f'/api/questions/{nq_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], nq_id)

    def test_post_empty_question(self):
        """POST a new question without a question or answer, should fail 400"""
        empty_question = {
            "question": "          ",
            "answer": "           ",
            "category": "6",
            "difficulty": 1
        }
        res = self.client().post('/api/questions', json=empty_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_get_questions_of_category(self):
        """Test GET request of questions only by a certain category"""
        # Get all the questions for Geography (id=3), should be 3 questions
        res = self.client().get('/api/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)

        # Get questions for category 100 (doesn't exist, should 404)
        res = self.client().get('/api/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_question_search(self):
        """Search for a term in a question"""
        res = self.client().post('/api/questions', json={"searchTerm": "  PeaNUT  "})   # Who invented Peanut Butter?
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['questions'][0]['id'], 12)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()