# Full Stack API Course Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

I have completed the trivia app by developing an API for the backend that the frontend can call to:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.


## Quick Start

### Frontend
```bash
npm install
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view the Trivia app in the browser.

### Backend

To set up the backend API server:
```bash
# Install requirements in a virtual environment
pip install -r requirements.txt
# Set up the trivia database
psql -U postgres trivia < trivia.psql
# Prepare the Flask app to run.  Use 'set' instead of 'export' on Windows
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

To run unit tests of the backend API server instead:
```bash
createdb -U postgres trivia_test
psql -U postgres trivia_test < trivia.psql
python test_flaskr.py
```

### More details...

If you have any issues with the above, or for more details on getting started, read the READMEs in order to get the frontend and backend up and running.  Both are complete with full functionality.

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)



# API Documentation

## Simple and RESTful

The API for the Trivia project is relatively simple.  All calls are made with either `GET`, `POST`, or `DELETE` HTTP methods.  No API key is needed.

CORS is enabled on all API routes to enable other websites (such as the Trivia frontend) to call it, since it will not fall under the same-origin policy (even on the same computer, the hosts will be different port numbers).  CORS is only relaxed on `/api/` URL endpoints to limit scope.

## Endpoint conventions and Error codes

All responses are returned in JSON format and all contain at the very least, a `"success"` key, which will return either `True` or `False`.

When error codes are returned (currently `400`, `404`, `422`, and `500`), they will return in a format like the following 404 example:

```bash
{
    "success": False,
    "error": 404,
    "message": "Not found"
}
```

## API Objects

The Trivia API is made up of just two types, Categories and Questions.  

- Categories
    - Categories for Trivia questions can be one of 6 possible values: Science, Art, Geography, History, Entertainment, and Sports
- Questions
    - Trivia questions contain the question itself, the category it belongs to, the difficulty (on a scale of 1 to 5), and an answer


##  GET '/api/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs

##### EXAMPLE `curl http://localhost:5000/api/categories`

```bash
{
    "categories": {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    "success": true
}
```


##  GET '/api/questions'

- Gets a list of all the trivia questions across all categories
- Paginates response to limit to 10 results per page
- Append URL parameter `?page=<num>` to return a different page (defaults to page 1)
- Request Arguments: None
- Returns: All categories, a list of questions with key value pairs, success status, and total number of questions in database

##### EXAMPLE `curl http://localhost:5000/api/questions?page=2`

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Blood", 
      "category": "1", 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    ... TRUNCATED FOR BREVITY ...
    {
      "answer": "6", 
      "category": "6", 
      "difficulty": 1, 
      "id": 24, 
      "question": "How many points is a touchdown worth?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```


##  DELETE '/api/questions/<question_id>'

- Deletes a question by id
- Request Arguments: question id
- Returns: Success status and id of deleted question if successful

##### EXAMPLE `curl -X DELETE http://localhost:5000/api/questions/4`

```bash
{
    'deleted': 4,
    'success': true
}
```  


##  POST '/api/questions'

- This endpoint performs two functions
    - Creates a new question via a form
    - Searches questions by search term form

### Creating a new question

- Request Arguments: question data via `application/json` type
- Returns: Success status and id of newly created question if successful

##### EXAMPLE `curl -X POST http://localhost:5000/api/questions -H "Content-Type: application/json" -d '{"question": "How many points is a touchdown worth?", "answer": "6", "category": "6", "difficulty": 1}'`

```bash
{
    "success": true,
    "added": 24
}
```

### Searching questions via search term form

- Request Arguments: search term data via `application/json` type
- Returns: Success status and a list of questions and their data that met the search results

##### EXAMPLE `curl -X POST http://localhost:5000/api/questions -H "Content-Type: application/json" -d '{"searchTerm": "points"}'`

```bash
{
  "questions": [
    {
      "answer": "6", 
      "category": "6", 
      "difficulty": 1, 
      "id": 24, 
      "question": "How many points is a touchdown worth?"
    }
  ], 
  "success": true
}
```


##  GET '/api/categories/<category_id>/questions'

- Gets all the questions based on a particular category
- Request Arguments: category_id
- Returns: Success status and list of questions for that category, plus a total question count of the non-paginated results

##### EXAMPLE `curl http://localhost:5000/api/categories/3/questions`

```bash
{
  "categories": {
    "id": 3, 
    "type": "Geography"
  }, 
  "current_category": 3, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": "3", 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": "3", 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": "3", 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```  
        

##  POST '/api/quizzes'

- Enables the playing of a Trivia game
    - Returns a random question for a given category that has not been asked already
    - Can return questions randomly chosen from a particular category, or across all of them
- Request Arguments: quiz category and a list of previously asked questions (client app must keep track of this), encoded in `application/json` format
- Returns: success status and if successful, a random question.  If there are no more questions to return in that category, the API just returns success but with no question key/value pair, which tells the frontend the quiz is over.

##### EXAMPLE of getting a question from all categories (category 0), and none have been asked yet `curl -X POST http://localhost:5000/api/quizzes -H "Content-Type: application/json" -d '{previous_questions: [], quiz_category: {type: "click", id: 0}}'`

```bash
{
  "question": {
    "answer": "Uruguay", 
    "category": "6", 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }, 
  "success": true
}
``` 

##### EXAMPLE of getting a question from the History category (category 4), and there are no more questions left in that category `curl -X POST http://localhost:5000/api/quizzes -H "Content-Type: application/json" -d '{previous_questions: [5, 9, 23, 12], quiz_category: {type: "History", id: "4"}}'`

```bash
{
  "success": true
}
```
