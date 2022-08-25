from db import db
from datetime import datetime

note_tag = db.Table('note_tag',
                    db.Column('note_id', db.Integer, db.ForeignKey('notes.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                    db.UniqueConstraint('note_id', 'tag_id', name='UC_note_id_tag_id')
                    )


class NoteModel(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.String(50))
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    tag = db.relationship('TagModel', secondary=note_tag, backref='notes', lazy='dynamic', cascade='all')

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def json(self):
        return {'title': self.title,
                'body': self.body,
                'tags': list(f'#{tags.name}' for tags in self.tag),
                'date': f'{self.created_at}'
                }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def get_note_tag(cls, title):
        note_tag_list = list(tag for tag in title.tag)
        if note_tag_list:
            return note_tag_list[0]
        return None

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def add_note_to_tag(cls, title, tag_name):
        title.tag.append(tag_name)
        db.session.commit()

    @classmethod
    def rem_note_from_tag(cls, title, tag_name):
        title.tag.remove(tag_name)
        db.session.commit()
