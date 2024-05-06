from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required.')  # Raise an error if name is empty

        # Check if the name is already present in the database
        existing_record = Author.query.filter(Author.name == name).first()
        if existing_record and existing_record.id != self.id:
            raise ValueError('Name must be unique.')  # Raise an error if name is not unique

        return name
    

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError('Phone number is required.')  # Raise an error if phone number is empty

        # Remove non-digit characters and check if the length is 10
        cleaned_phone_number = ''.join(filter(str.isdigit, phone_number))
        if len(cleaned_phone_number) != 10:
            raise ValueError('Phone number must be 10 digits long.')  # Raise an error if length is not 10

        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters long')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary is a maximum of 250 characters long')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        categories = ['Fiction', 'Non-Fiction']
        if category not in categories:
            raise ValueError("Category must be fiction of non-fiction")
        return category

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title must exist")
        
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]

        # Check if the title contains any of the clickbait phrases
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Title must contain one of the following: "Won\'t Believe", "Secret", "Top", "Guess"')

        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
