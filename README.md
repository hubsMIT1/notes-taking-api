# Notes Taking Rest API

This is a Django REST framework project that allows users to create, update, share, and delete notes, as well as view the version history of the notes.

## Installation

- clone this repository or download it as a zip file.

- To install the required packages, run the following command in the project directory:
```
pip install -r requirements.txt
```

- To `TEST`, run the following commands:
  
```
    python manage.py test notes
```
- To set up the database, run the following commands:

```
python manage.py makemigrations
python manage.py migrate
```

To create a superuser account, run the following command and follow the prompts:

```
python manage.py createsuperuser
```

- To run the development server, run the following command:

```
python manage.py runserver
```

## Usage
To use the API endpoints, you need to have a valid user account and an authentication token. You can use the admin panel or the signup endpoint to create a user account, and the login endpoint to get the token.

### Register
`BASE_URL/register/`: This endpoint allows you to register a new user account. It accepts a POST request with the following json data:

```
JSON
{   
    "username": "<username>", 
    "email": "<email>",
    "password": "<password>"
}

```

### Login
`BASE_URL/login/`: This endpoint allows you to log in as an existing user and get the authentication token. It accepts a POST request with the following json data:
```
JSON
{
    "username": "<username>", 
    "password": "<password>"
}
```

You can use any HTTP client, such as Postman or curl, to send requests to the API endpoints. You need to include the authentication token in the header of your requests, using the following format:

```Authorization: Token <token>```

where `<token>` is the token you received from the login endpoint.

#### The following are the available API endpoints and their usage:

### Create a new note
`/notes/create` POST: This endpoint allows you to create a new note. It accepts a POST request with the following json data:
```
JSON

{
    "title": "<title>",
    "content": "<content>"
}

```

### Retrieve note
`/notes/<int:id>` GET: This endpoint allows you to retrieve a specific note by its id.
> id: The id of the note you want to access. It must be an integer value, such as 1, 2, 3, etc.


### Update or Delelte 
`/notes/<int:id>` PUT or PATCH | DELETE: This endpoint allows you to update, or delete a specific note by its id.

For the PUT or PATCH request, the following json data is required:
```
JSON
{
    "title": "<title>",
    "content": "<content>"
}
```

### Share Note
`/notes/<int:id>/share` POST: This endpoint allows you to share a note with other users. It accepts a POST request with the following json data:
```
JSON
{
    "users": [<users>]
}

```
> where `<id>` is the id of the note you want to share, and `<users>` is a list of usernames or emails of the users you want to share the note with.

### Get all the changes

`/notes/version-history/int:id/` GET: This endpoint allows you to get the version history of a note by its id. It accepts a GET request.