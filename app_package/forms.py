from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField \
                    ,SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length

wksht_codes = [('A000000','A'),('A10000','A-1'),('A200000','A-2'),('A30000A','A-3 Part A'),
               ('A30000B','A-3 Part B'),('A30000C','A-3 Part C'),('A400001','A-4 Part 1'),
               ('A400002','A-4 Part 2'),('B000000','B'),('B100000','B-1'),('C000000','C'),
               ('D000000','D'),('E000001','E Part 1'),('E000002','E Part 2'),('E100001','E-1 Part 1'),
               ('E100002','E-1 Part 2'),('F000000','F'),('F100000','F-1'),('S000001','S Part 1'),
               ('S000002','S Part 2'),('S000003','S Part 3'),('S100000','S-1'),('S200000','S-2')]

fac_info_choices = [('medicare_id','Medicare ID'),('facility_name','Facility Name'),('address','Address'),
                    ('city','City'),('county','County'),('zip_code','Zip Code'),('state','State'),
                    ('non_for_profit','Non/For-Profit'),('dialysis_chain','Dialysis Chain')]

utilization_choices = []
finance_choices = [('net_patient_revenue','Net Patient Revenue'),('operating_expenses','Operating Expenses'),
                   ('net_income_patient_services','Net Income Patient Services'),('covid_19_income','Covid-19 Income'),
                   ('other_income','Other Income'),('net_income','Net Income')]

state_choices = ['AK','AL', 'AR','AS','AZ','CA','CO','CT','DC','DE','FL','GA','GU','HI','IA','ID','IL' 
                 ,'IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MP','MS','MT','NC','ND','NE','NH'
                 ,'NJ','NM','NV','NY','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VA','VI'
                 ,'VT','WA','WI','WV','WY']

#forms for custom data
class FieldsForm(FlaskForm):
    worksheet = SelectField('Worksheet Code',choices = wksht_codes, validators=[DataRequired()])
    line_number = DecimalField('Line Number', places=2, validators=[DataRequired()])
    column_number = DecimalField('Column Number', places=2,validators=[DataRequired()])
    var_name = StringField('Variable Name', validators=[DataRequired(),Length(min=0,max=40)])
    submit = SubmitField('Add to Cart')
 
class ClearForm(FlaskForm):
    clear = SubmitField('Clear Selection', validators=[DataRequired()])

class DownloadForm(FlaskForm):
    download = SubmitField('Download Dataset', validators=[DataRequired()])

#forms for preset data
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PresetInfoForm(FlaskForm):
    facility_info = MultiCheckboxField('Facility Information', choices=fac_info_choices)
    utilization = MultiCheckboxField('Utilization Data', choices = utilization_choices)
    finance = MultiCheckboxField('Financial Statement', choices = finance_choices)
    submit = SubmitField('Add Variables')

class FacFilterForm(FlaskForm):
    years = [(i,i) for i in range(2022,2010,-1)]
    year_field = MultiCheckboxField('Year', choices=years)
    states = [(i,i) for i in state_choices]
    state_field = MultiCheckboxField('State/Territory', choices=states)
    submit = SubmitField('Add Filters')

"""
class WorksheetForm(FlaskForm):
    worksheet = SelectField('Worksheet Code', choices = wksht_codes, validators=[DataRequired()])
    submit = SubmitField('Submit')
"""
