from app import db 

class Category(db.Model):
    """This class represents the bucketlist table. """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    recipe_name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self,category_name):
        """initialize with username and password"""
        self.category_name = category_name
        

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Category.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Category: {}>".format(self.name)