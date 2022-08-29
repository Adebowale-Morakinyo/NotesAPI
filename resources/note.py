from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.note import NoteModel
from models.tag import TagModel


class Note(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('body',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    #@jwt_required()
    def get(self, note_title):
        note = NoteModel.find_by_title(note_title)
        if note:
            return note.json()
        return {'message': 'Note not found'}, 404

    def post(self, note_title):
        if NoteModel.find_by_title(note_title):
            return {'message': "A note titled '{}' already exists.".format(note_title)}, 400

        data = Note.parser.parse_args()

        note = NoteModel(note_title, data['body'])

        try:
            note.save_to_db()
        except:
            return {"message": "An error occurred inserting the note."}, 500

        return note.json(), 201

    @jwt_required()
    def delete(self, note_title):
        note = NoteModel.find_by_title(note_title)

        if note:
            tag = NoteModel.get_note_tag(note)
            if tag:
                NoteModel.rem_note_from_tag(note, tag)
                note.delete_from_db()
                return {'message': 'Note deleted'}
            note.delete_from_db()
            return {'message': 'Note deleted'}

        return {'message': 'Note not found'}, 404

    #@jwt_required()
    def put(self, note_title):
        data = Note.parser.parse_args()

        note = NoteModel.find_by_title(note_title)

        if note is None:
            note = NoteModel(note_title, data['body'])
        else:
            note.body = data['body']

        note.save_to_db()
        return note.json()


class NoteList(Resource):
    def get(self):
        return {'Notes': [note.json() for note in NoteModel.find_all()]}


class NoteTag(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('note_title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self, tag_name):
        data = NoteTag.parser.parse_args()
        tag = TagModel.find_by_name(tag_name)
        note = NoteModel.find_by_title(data['note_title'])
        note_still_tagged = NoteModel.get_note_tag(note)

        if tag and note:
            if note_still_tagged is None:
                NoteModel.add_note_to_tag(note, tag)
                return {'message': 'Note tagged.'}
            return {'message': "Note titled {} with tag '{}' already exist".format(data['note_title'], tag_name)}, 400
        return {'message': 'Tag or note does not exist.'}, 404


class Untag(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tag_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def delete(self, note_title):
        data = Untag.parser.parse_args()
        tag_name = data['tag_name']
        tag = TagModel.find_by_name(tag_name)
        note = NoteModel.find_by_title(note_title)
        note_still_tagged = NoteModel.get_note_tag(note)

        if tag and note:
            if note_still_tagged:
                NoteModel.rem_note_from_tag(note, tag)
                return {'message': 'Tag removed.'}
            return {'message': " '{}' note with tag '{}' does not exist".format(note_title, tag_name)}, 400
        return {'message': 'Tag or note does not exist.'}, 404
