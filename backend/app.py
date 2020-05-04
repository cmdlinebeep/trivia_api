import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Helper Functions
###########################

# Pagination
def paginate(request, selection):
    page = request.args.get('page', 1, type=int)    # 1 is the default if not given
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # It's more efficient to do the slicing on selection rather than further post-processing
    # by slicing the questions list next (as given in class example code)
    questions = [ question.format() for question in selection[start:end] ]
    return questions


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

    # API-digestible error handlers
    # These override the default HTML response when we call abort
    ###############################
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        })

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        })

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        })


    @app.route('/api/categories')
    def get_categories():
        try:
            # Simple request, should return with no issues, but catch failure case
            categories = Category.query.all()
            cat_dict = {cat.id:cat.type for cat in categories}
        
            return jsonify({
                "success": True,
                "categories": cat_dict
            })
        except:
            abort(500)  # Internal server error if can't do this


    @app.route('/api/questions')
    def get_questions():
        questions = Question.query.all()
        total_questions = len(questions)

        # q_list = [q.format() for q in questions]  # Unpaginated
        q_list = paginate(request, questions)
        
        categories = Category.query.all()
        cat_dict = {cat.id:cat.type for cat in categories}
        
        if len(q_list) == 0:
            # Requested a page past what exists
            abort(404)

        return jsonify({
            'success': True,
            'questions': q_list,
            'total_questions': total_questions,
            'categories': cat_dict,
            'current_category': None
        })


    @app.route('/api/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        question = Question.query.get(q_id)

        if not question:
            # Question id doesn't exist
            abort(404)
        else:
            # Exists, try to delete it
            try:
                question.delete()   # Has own method

                return jsonify({
                    'success': True,
                    'deleted': q_id
                })
            except:
                abort(422)  # Understood the request and it was formatted properly, but was unable to process request
                
    
    @app.route('/api/questions', methods=['POST'])
    def add_question():
        '''This endpoint not only POSTs new questions, but is also how the search terms
        on questions works, so we need to handle both cases here'''
        form_data = request.json

        if "searchTerm" in form_data:
            search_term = form_data['searchTerm'].strip()

            # Use filter, not filter_by when doing LIKE search (i=insensitive to case)
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()   # Wildcards search before and after
            
            # Still good idea to paginate since search could return a ton (entire list if you search "", 
            # which project doesn't exclude).  However Search Questions view in Frontend doesn't already include
            # support for pagination, so this time I won't do it (or you can't see all valid search results).
            #q_list = paginate(request, questions)
            q_list = [q.format() for q in questions]

            return jsonify({
                "success": True,
                "questions": q_list
            })
        
        else:
            # Otherwise, adding a new question through form

            # Check for errors with the submission
            if (form_data['question'].strip() == "") or (form_data['answer'].strip() == ""):
                # Don't populate blanks, return a bad request error
                abort(400)

            try:
                new_question = Question(question=form_data['question'].strip(), answer=form_data['answer'].strip(), \
                    category=form_data['category'], difficulty=form_data['difficulty'])
                new_question.insert()
            except:
                # Issue creating new question?  422 means understood the request but couldn't do it
                abort(422)

            return jsonify({
                "success": True,
                "added": new_question.id
            })


    @app.route('/api/categories/<int:cat_id>/questions')
    def get_category_questions(cat_id):
        '''GET all the questions based on a particular category'''
        questions = Question.query.filter_by(category=str(cat_id)).all()

        q_list = paginate(request, questions)

        if len(q_list) == 0:
            # Requested a page past what exists
            abort(404)

        return jsonify({
            'success': True,
            'questions': q_list,
            'total_questions': len(questions),
            'categories': Category.query.get(cat_id).format(),
            'current_category': cat_id
        })


    @app.route('/api/quizzes', methods=['POST'])
    def play_quiz():

        # From Developer Tools, examples of the Request Payload looks like this:
        # {previous_questions: [], quiz_category: {type: "click", id: 0}} # 0 is ALL
        # {previous_questions: [], quiz_category: {type: "Art", id: "2"}}
        # {previous_questions: [17, 16, 18], quiz_category: {type: "Art", id: "2"}}

        # Get questions of category.  Category 0 is ALL.
        request_data = request.json
        try:
            request_cat = request_data['quiz_category']['id']
        except:
            # Category must be supplied in this format
            abort(400)

        if request_cat == 0:
            # Get questions from all categories
            questions = Question.query.all()
        else:
            # Get questions for only one category
            questions = Question.query.filter_by(category=str(request_cat)).all()

        # Format the questions
        questions = [q.format() for q in questions]
        
        # print("Questions before filtering:")
        # for q in questions:
        #     print(q['id'])

        # First prune out the questions from the set that have already been asked.
        # This is much more performant (with larger datasets) than randomly iterating over and over picking
        # questions and then testing if they've been asked before.  Can't guarantee maximum latency that way.
        # For example, could get sequence of several identical random numbers in a row.
        try:
            prev_qs = request_data['previous_questions']    # This is a list by id
        except:
            # Previous questions must be supplied
            abort(400)
        
        # print("Previous questions:")
        # print(prev_qs)
        
        # Prune the list
        pruned_qs = []
        for q in questions:
            if q['id'] not in prev_qs:
                pruned_qs.append(q)

        # print("Questions after filtering:")
        # for q in pruned_qs:
        #     print(q['id'])

        # Make sure this isn't an empty set (played all the questions)
        # If we've used al the questions up, return without a question to inform frontend quiz is over.
        if len(pruned_qs) == 0:
            return jsonify({
                'success': True
            })

        # Otherwise, pick a random question from the pruned set
        question = random.choice(pruned_qs)

        # print(f'Picked question: {question}')

        # Now return it
        return jsonify({
            'success': True,
            'question': question
        })


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