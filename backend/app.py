import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Sets up CORS to allow '*' for origins on all API routes and resources.
    # I changed the frontend routes to include /api/ in the path to make this
    # a little more secure by being less permissive than the broadest strokes (CORS(app))
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Set Access-Control-Allow headers after each request
    # (after_request decorator runs after the route handler for a request, but 
    # keep in mind it MODIFIES the response.
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    # Helper function for pagination
    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)    # 1 is the default if not given
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # It's more efficient to do the slicing on selection rather than further post-processing
        # by slicing the questions list next (as given in class example code)
        questions = [ question.format() for question in selection[start:end] ]
        return questions


    @app.route('/api/categories')
    def get_categories():
        categories = Category.query.all()
        cat_dict = {cat.id:cat.type for cat in categories}
        
        #FIXME: handle errors
        
        return jsonify({
            "success": True,
            "categories": cat_dict
        })


    @app.route('/api/questions')
    def get_questions():
        questions = Question.query.all()
        total_questions = len(questions)

        # q_list = [q.format() for q in questions]  # Unpaginated
        q_list = paginate(request, questions)
        
        categories = Category.query.all()
        cat_dict = {cat.id:cat.type for cat in categories}
        
        # FIXME: handle errors

        return jsonify({
            'success': True,
            'questions': q_list,
            'total_questions': total_questions,
            'categories': cat_dict,
            'current_category': None
        })


    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''