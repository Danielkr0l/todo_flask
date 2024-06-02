from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_deadline(self, field):

        if datetime.combine(field.data, datetime.min.time()) <= datetime.combine(datetime.today(), datetime.min.time()):
            raise ValidationError("The deadline must be in the future.")