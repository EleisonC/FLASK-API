from app import db 

class Recipe(db.Model):
    """This class represents the bucketlist table. """
    __tablename__ = "recipe_name"

    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(255))
    instruction = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self,recipe_name,instruction):
        """initialize with recipe_name and instruction"""
        self.recipe_name = recipe_name
        self.instruction = instruction
        

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Recipe.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Recipe: {}>".format(self.name)