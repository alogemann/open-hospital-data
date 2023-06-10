from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class FieldsForm(FlaskForm):
    worksheet = StringField('Worksheet Code', validators=[DataRequired(),Length(min=7,max=7)])
    line_number = StringField('Line Number', validators=[DataRequired(), Length(min=1, max=6)])
    column_number = StringField('Column Number', validators=[DataRequired(), Length(min=1,max=6)])
    var_name = StringField('Variable Name', validators=[DataRequired(),Length(min=0,max=20)])
    submit = SubmitField('Add to Cart')
 
class ClearForm(FlaskForm):
    clear = SubmitField('Clear', validators=[DataRequired()])

class CreateForm(FlaskForm):
    create = SubmitField('Create Dataset', validators=[DataRequired()])

class DownloadForm(FlaskForm):
    download = SubmitField('Download Dataset', validators=[DataRequired()])