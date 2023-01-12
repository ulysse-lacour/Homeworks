from sqlalchemy.dialects.postgresql import JSON
from project.settings import DB_ORM as db
from project.models.abstract import SerializableModel


class Image(db.Model, SerializableModel):
    '''

    '''
    id = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    color: str = db.Column(db.String(30), nullable=False)
    details = db.Column(JSON)
    accepted: bool = db.Column(db.Boolean, default=False)

    non_serializable_fields = {
        'details',
    }

    @property
    def id_str(self):
        return f"<Image: {self.id} - {self.name}>"
