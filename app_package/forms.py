from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, SelectMultipleField \
                    ,widgets
from wtforms.validators import DataRequired, Length

wksht_codes = [('A000000','A'),('A10000','A-1'),('A200000','A-2'),('A30000A','A-3 Part A'),
               ('A30000B','A-3 Part B'),('A30000C','A-3 Part C'),('A400001','A-4 Part 1'),
               ('A400002','A-4 Part 2'),('B000000','B'),('B100000','B-1'),('C000000','C'),
               ('D000000','D'),('E000001','E Part 1'),('E000002','E Part 2'),('E100001','E-1 Part 1'),
               ('E100002','E-1 Part 2'),('F000000','F'),('F100000','F-1'),('S000001','S Part 1'),
               ('S000002','S Part 2'),('S000003','S Part 3'),('S100000','S-1'),('S200000','S-2')]

fac_info_choices = [('prvdr_ccn','Medicare ID'),('prvdr_name','Facility Name'),('prvdr_addr','Address'),
                    ('prvdr_city','City'),('prvdr_county','County'),('prvdr_zip','Zip Code'),('prvdr_state','State'),
                    ('prvdr_cbsa','CBSA'),('type_control','Non/For-Profit'),('chain_org','Chain (Y/N)'),
                    ('chain_name','Dialysis Chain')]

utilization_choices = []
finance_choices = []

#forms for custom data
class FieldsForm(FlaskForm):
    worksheet = SelectField('Worksheet Code',choices = wksht_codes, validators=[DataRequired()])
    line_number = DecimalField('Line Number', places=2, validators=[DataRequired()])
    column_number = DecimalField('Column Number', places=2,validators=[DataRequired()])
    var_name = StringField('Variable Name', validators=[DataRequired(),Length(min=0,max=20)])
    submit = SubmitField('Add to Cart')
 
class ClearForm(FlaskForm):
    clear = SubmitField('Clear Selection', validators=[DataRequired()])

class CreateForm(FlaskForm):
    create = SubmitField('Create Dataset', validators=[DataRequired()])

class DownloadForm(FlaskForm):
    download = SubmitField('Download Dataset', validators=[DataRequired()])

#forms for preset data
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class FacInfoForm(FlaskForm):
    facility_info = MultiCheckboxField('Facility Information', choices=fac_info_choices)
    utilization = MultiCheckboxField('Utilization', choices = utilization_choices)
    finance = MultiCheckboxField('Financial', choices = finance_choices)
    submit = SubmitField('Next')

class FacFilterForm(FlaskForm):
    years = [(i,i) for i in range(2012,2022)]
    year_field = MultiCheckboxField('Year', choices=years)
    submit = SubmitField('Submit')

"""
class WorksheetForm(FlaskForm):
    worksheet = SelectField('Worksheet Code', choices = wksht_codes, validators=[DataRequired()])
    submit = SubmitField('Submit')
"""
