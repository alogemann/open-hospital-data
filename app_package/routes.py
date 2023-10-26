import pandas as pd
from flask import render_template, redirect, send_file, url_for, request
from sqlalchemy import text, select
from app_package import app, db
from app_package.forms import ClearForm, FieldsForm, CreateForm, DownloadForm, PresetInfoForm, FacFilterForm
from app_package.models import Report_field, Preset_Field, Year_Field, Fac_Info_Field
from app_package.helpers import format_field

@app.route('/f/<string:id>')
def facility(id):
    stmt = select(Fac_Info_Field).where(Fac_Info_Field.prvdr_ccn == id)
    result = db.session.execute(stmt)
    facility = result.all()[0][0]
    print(facility)
    return render_template('facility.html',facility=facility)



@app.get('/')
@app.get('/index')
def index():
    return render_template('index.html')

@app.route('/presets',methods=['GET','POST'])
def presets():

    preset_form = PresetInfoForm()

    if request.method=='GET':
        return render_template('presets.html', preset_form=preset_form)

    elif preset_form.validate_on_submit():
        for i in preset_form.data['facility_info']:
            new_preset = Preset_Field(preset_name = i,
                                      preset_src = 'fac_info')
            db.session.add(new_preset)
            db.session.commit()
        return(redirect(url_for('custom')))
    else:
        return '<h1>ERROR</h1>'

@app.route('/custom', methods=['GET','POST'])
def custom():

    fields_form = FieldsForm()
    clear_form = ClearForm()
    create_form = CreateForm()

    all_fields = Report_field.query.all()

    ##Get Request
    if request.method=='GET':
        return render_template('custom.html',
                               fields_form = fields_form,
                               clear_form = clear_form,
                               create_form = create_form,
                               all_fields = all_fields)

    ##Post Requests
    if fields_form.validate_on_submit():
        new_field = Report_field(var_name = fields_form.var_name.data,
                                    wksht_cd = fields_form.worksheet.data,
                                    line_num = format_field(fields_form.line_number.data),
                                    clmn_num = format_field(fields_form.column_number.data))
        db.session.add(new_field)
        db.session.commit()
        return redirect(url_for('custom'))
    
    elif clear_form.validate_on_submit():
        delete_fields = Report_field.__table__.delete()
        db.session.execute(delete_fields)
        db.session.commit()
        return redirect(url_for('custom'))
    
    elif create_form.validate_on_submit():
        return redirect(url_for('filter'))
    
    else:
        return '<h1>ERROR</h1>'

@app.route('/filter',methods=['GET','POST'])
def filter():
    fac_filter_form = FacFilterForm()

    if request.method == 'GET':
        return render_template('filter.html',fac_filter_form=fac_filter_form)
    elif request.method == 'POST':
        for i in fac_filter_form.data['year_field']:
            year_field = Year_Field(year = i)
            db.session.add(year_field)
            db.session.commit()
        return redirect(url_for('download'))
    else:
        return '<h1>ERROR</h1>'


@app.route('/download',methods=['GET','POST'])
def download():
    download_form = DownloadForm()

    if request.method == 'GET':
        return render_template('download.html', download_form = download_form)
    
    elif download_form.validate_on_submit():
        db.session.execute(text('CALL build_variables();'))
        db.session.commit()
        db.session.execute(text('CALL add_presets()'))
        db.session.commit()
        db.session.execute(text('CALL build_table();'))
        db.session.commit()
        db.session.execute(text('CALL year_filter();'))
        new_df = pd.DataFrame(db.session.execute(text('Select * from final_table')))
        new_df.to_csv('app_package/static/custom.csv',index=False)
        db.session.execute(text('CALL delete_tables();'))
        delete_reports = Report_field.__table__.delete()
        delete_years = Year_Field.__table__.delete()
        delete_presets = Preset_Field.__table__.delete()
        db.session.execute(delete_reports)
        db.session.execute(delete_years)
        db.session.execute(delete_presets)
        db.session.commit()
        return send_file('static/custom.csv',as_attachment=True)
    else:
        return '<h1>ERROR</h1>'

"""
@app.route('/custom_select', methods=['GET','POST'])
def custom_select():

    wksht_form = WorksheetForm()
    wksht_list = Worksheet_field.query.all()

    form_list = []
    for i in wksht_list:
        form_list.append(Report_field(worksheet = i))

    field_dict = {}
    for i in wksht_list:
        field_dict[i] = Report_field.query.all() #add where clause for whsht

    if request.method == 'GET':
        return render_template('custom_drop_down.html', 
                               wksht_form = wksht_form,
                               wksht_list = wksht_list,
                               form_list = form_list,
                               field_dict = field_dict)
    
    elif wksht_form.validate_on_submit():
        new_wksht = Worksheet_field(wksht_name = wksht_form.worksheet.data)
        db.session.add(new_wksht)
        db.session.commit()
        return redirect(url_for('custom_select'))
"""