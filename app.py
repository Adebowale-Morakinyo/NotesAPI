from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.note import Note, NoteList, NoteTag, Untag
from resources.tag import Tag, TagList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '51de0c692eb2684921d3cae1807651ef'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Note, '/note/<string:note_title>')
api.add_resource(Tag, '/tag/<string:name>')
api.add_resource(NoteList, '/notes')
api.add_resource(TagList, '/tags')
api.add_resource(NoteTag, '/addTo/<string:tag_name>')
api.add_resource(Untag, '/untag/<string:note_title>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(debug=True)
