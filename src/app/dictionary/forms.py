from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Dictionary


class Add_Word(FlaskForm):
    english_word = StringField('English Word', validators=[DataRequired(), Length(min=1, max=20)])
    german_article = StringField('Article', validators=[DataRequired(), Length(min=0,max=3)])
    german_word = StringField('German Word', validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('Add Word')

    def validate_english_word(self, english_word):
        engish_word = Dictionary.query.filter_by(english_word= english_word.data).first()
        if engish_word:
            raise ValidationError('Error: English word already exist in dictionary!') 
    
    def validate_german_word(self, german_word):
        german_word = Dictionary.query.filter_by(german_word = german_word.data).first()
        if german_word:
            raise ValidationError('Error: German word already exist in dictionary!') 


    