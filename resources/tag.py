from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.tag import TagModel


class Tag(Resource):

    #@jwt_required()
    def get(self, name):
        note = TagModel.find_by_name(name)
        if note:
            return note.json()
        return {'message': 'Tag not found'}, 404

    def post(self, name):
        if TagModel.find_by_name(name):
            return {'message': "A tag named '{}' already exists.".format(name)}, 400

        tag = TagModel(name)

        try:
            tag.save_to_db()
        except:
            return {"message": "An error occurred inserting the note."}, 500

        return tag.json(), 201

    @jwt_required()
    def delete(self, name):
        tag = TagModel.find_by_name(name)

        if tag:
            tag.delete_from_db()
            return {'message': 'Tag deleted'}

        return {'message': 'Tag not found'}

    #@jwt_required()
    def put(self, name):
        tag = TagModel.find_by_name(name)

        if tag is None:
            tag = TagModel(name)
        else:
            tag.name = name

        tag.save_to_db()
        return tag.json()


class TagList(Resource):
    def get(self):
        return {'Tags': [note.json() for note in TagModel.find_all()]}
