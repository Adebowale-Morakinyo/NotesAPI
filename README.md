 # NotesAPI
 ## REST-API using Python - Flask 
#### +Flask_SQLAlchemy &nbsp; +Flask_JWT &nbsp; +Flask_JWT_extended     
### And Flask-RESTful for more REST standard


## Description
Imagine an API where you can manage notes. A database in the background and all CRUD necessary for it work.

Users will be able to:
- Add, update and delete single notes
- Notes will contain the title, body, tags and date.
- Sort/Filter all notes by dates, titles and tags

And other necessary functionalities like user authentication, logging out and restrictions, token refreshing,etc

## Project Structure

- ## app.py
In app.py, the Flask application is initialized and configured. The API resources also set up.

This file is the entry point to the REST API.

- ## db.py
In this file the database Python object was created so that other files can import it. All other files import the database variable from this file.

The reason for creating a separate file containing just this is precisely, so it's easier to import, and to avoid Python's circular imports.

- ## Models
### models/note.py
The note_tag table (implementing many to many relationship between the tags and notes). So a note can be tagged by any number of tags and a tag can be used for bunch of notes.  

The NoteModel contains a definition of what data the application deals with, and ways to interact with that data. Essentially it is a class with four properties:

id;<br>
title;<br>
body; and<br>
created_at.<br>

Methods in the class can be used to find notes by title, save them to the database, or retrieve them. Other methods are used to interact with the tag table.

### models/tag.py
The TagModel is another definition of data the application deals with. It contains two properties:

id; and<br>
name.

In addition, because every NoteModel has a tag property, TagModels are able to use SQLAlchemy to find the notes that have been tagged to the ItemModel's id in the note_tag Table. It can do that by using SQLAlchemy's db.relationship().


### models/user.py
The UserModel is the final data definition in the API. They contain:

id;
username; and
password.


- ## Resources
### resources/note.py
Finally, the resource is what defines how clients will interact with the REST API. In the resource the endpoints where clients will have to send requests is defined, as well as any data they have to send in that request.

For example, you could define that when clients send a GET request to /note/coding, the API will respond with data of a note titled coding. That data could be loaded from the database.

>TIP

>In Flask-RESTful we define a class for each Resource, and each Resource can have one Python method for each HTTP method that it should be able to respond to.

In addition, resources/note.py also defines a NoteList resource which can be used to retrieve multiple notes at once via the API. A NoteTag resource, so a user can add a note to a tag. And an Untag resource to remove a tag from a note.

### resources/tag.py
In a similar way to the Note resource, the Tag resource defines how users interact with the API.

Users will be able to get tags, create them, and delete them. Similarly, a TagList resource is defined to retrieve all tags in the API.


### resources/user.py
These resources are quite different from the other two because they do not only deal with creating and updating data in the application, they also deal with various user flows like authentication, token refresh, log outs, and more.


## Endpoints
### 1) GET/notes
This gets all the data(notes) from the Note table of from the database and return it in json format (array of objects)

e.g. looks like this...
```
{
    "Notes": [
        {
            "title": "REST API",
            "body": "Flexible in terms of data format and structure.",
            "tags": [
                "#apis",
                "#python"
            ],
            "date": "2022-08-24 22:01:46.358657"
        },
        {
            "title": "GRAPH API",
            "body": "Solves over_fetching and under_fetching.",
            "tags": [
                "#apis"
            ],
            "date": "2022-08-24 23:03:32.017294"
        }
    ]
}
```
## 2) GET /note/<note_title>
This gets all the data of the given http parameter(note_title) of from the database and return it in json format (array of objects)

e.g. GET {{url}}/note/REST API gives...
```
{
    "title": "REST API",
    "body": "Flexible in terms of data format and structure.",
    "tags": [
        "#apis",
        "#python"
    ],
    "date": "2022-08-24 22:01:46.358657"
}
```

## 3) POST /note/<note_title>
This creates note with given http parameter(note_title) as the note title and the body from received json data. Then stores it in the database and return its data in json format (array of objects).

This resource accept data in json format

Header
- Key: Content-Type  
- Value =  application/json

Body
>{ <br>&nbsp; &nbsp; &nbsp; "body" : "Enter body of the note"<br>}

e.g 
Imagine the the body has been filled <br>
POST {{url}}/note/REST API gives...
```
{
    "title": "REST API",
    "body": "Flexible in terms of data format and structure.",
    "tags": [],
    "date": "2022-08-24 22:01:46.358657"
}
```
Bonus : The date is autogenerated when created

# This is still under developement ...