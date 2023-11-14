import pandas as pd
from flask import render_template, redirect, send_file, url_for, request, flash
from sqlalchemy import text, select, desc, exc
from app_package import app, db
from app_package.forms import ClearForm, FieldsForm, DownloadForm, PresetInfoForm, FacFilterForm
from app_package.models import Report_field, Field_presets, Year_Field, Fac_Info_Field, State_Field, Chain_Field
from app_package.helpers import format_field

#home route
@app.get('/')
@app.get('/index')
def index():
    return render_template('index.html')

@app.route('/presets',methods=['GET','POST'])
def presets():

    preset_form = PresetInfoForm()
    clear_form = ClearForm()
    all_fields = Report_field.query.all()

    #get requests
    if request.method=='GET':
        return render_template('presets.html'
                               ,preset_form=preset_form
                               ,clear_form=clear_form
                               ,all_fields=all_fields)

    #post requests

    #clear variable list
    elif clear_form.validate_on_submit():
        delete_fields = Report_field.__table__.delete()
        db.session.execute(delete_fields)
        db.session.commit()
        return redirect(url_for('presets'))
    
    #add variable presets to report_field table
    elif preset_form.validate_on_submit():
        for key in preset_form.data.keys():
            if key in ['csrf_token','submit']:
                continue
            for i in preset_form.data[key]:
                stmt = select(Field_presets).where(Field_presets.var_name == i)
                field = db.session.scalars(stmt).first()
                new_field = Report_field(var_name = field.var_name
                                        ,wksht_cd = field.wksht_cd
                                        ,line_num = field.line_num
                                        ,clmn_num = field.clmn_num)
                db.session.add(new_field)
                try:
                    db.session.commit()
                except exc.IntegrityError:
                    db.session.rollback()
                    flash(f'{i} already selected')
        return(redirect(url_for('presets')))
    else:
        return '<h1>ERROR</h1>'

@app.route('/custom', methods=['GET','POST'])
def custom():

    fields_form = FieldsForm()
    clear_form = ClearForm()
    all_fields = Report_field.query.all()

    ##Get Request
    if request.method=='GET':
        return render_template('custom.html',
                               fields_form = fields_form,
                               clear_form = clear_form,
                               all_fields = all_fields)

    ##Post Requests
    if fields_form.validate_on_submit():
        new_field = Report_field(var_name = fields_form.var_name.data,
                                    wksht_cd = fields_form.worksheet.data,
                                    line_num = format_field(fields_form.line_number.data),
                                    clmn_num = format_field(fields_form.column_number.data))
        db.session.add(new_field)

        try:
            db.session.commit()
        except exc.IntegrityError:
            pass #send message to user

        return redirect(url_for('custom'))
    
    elif clear_form.validate_on_submit():
        delete_fields = Report_field.__table__.delete()
        db.session.execute(delete_fields)
        db.session.commit()
        return redirect(url_for('custom'))
    
    else:
        return '<h1>ERROR</h1>'

@app.route('/filter',methods=['GET','POST'])
def filter():

    fac_filter_form = FacFilterForm()
    clear_form = ClearForm()

    years = [i.year for i in Year_Field.query.all()]
    states = [i.state for i in State_Field.query.all()]
    chains = [i.chain for i in Chain_Field.query.all()]

    if request.method == 'GET':
        return render_template('filter.html'
                               ,fac_filter_form=fac_filter_form
                               ,clear_form=clear_form
                               ,years=years
                               ,states=states
                               ,chains=chains)
    elif clear_form.validate_on_submit():
        delete_years = Year_Field.__table__.delete()
        db.session.execute(delete_years)
        delete_states = State_Field.__table__.delete()
        db.session.execute(delete_states)
        delete_chains = Chain_Field.__table__.delete()
        db.session.execute(delete_chains)
        db.session.commit()
        return redirect(url_for('filter'))
    elif request.method == 'POST':
        for i in fac_filter_form.data['year_field']:
            year_field = Year_Field(year = i)
            db.session.add(year_field)
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash(f'{i} already selected')
        for i in fac_filter_form.data['state_field']:
            state_field = State_Field(state = i)
            db.session.add(state_field)
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash(f'{i} already selected')
        for i in fac_filter_form.data['chain_field']:
            chain_field = Chain_Field(chain = i)
            db.session.add(chain_field)
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash(f'{i} already selected')
        return redirect(url_for('filter'))
    else:
        return '<h1>ERROR</h1>'


@app.route('/download',methods=['GET','POST'])
def download():
    download_form = DownloadForm()

    years = [i.year for i in Year_Field.query.all()]
    states = [i.state for i in State_Field.query.all()]
    chains = [i.chain for i in Chain_Field.query.all()]

    all_fields = Report_field.query.all()

    if request.method == 'GET':
        print(years)
        print(states)
        print(chains)
        return render_template('download.html'
                               ,download_form = download_form
                               ,all_fields=all_fields
                               ,years=years
                               ,states=states
                               ,chains=chains)
    
    elif download_form.validate_on_submit():
        db.session.execute(text('CALL build_variables();'))
        db.session.commit()
        db.session.execute(text('CALL build_table();'))
        db.session.commit()
        db.session.execute(text('CALL year_filter();'))
        db.session.commit()
        new_df = pd.DataFrame(db.session.execute(text('Select * from final_table')))
        new_df.to_csv('app_package/static/data/custom.csv',index=False)
        db.session.execute(text('CALL delete_tables();'))
        delete_reports = Report_field.__table__.delete()
        delete_years = Year_Field.__table__.delete()
        delete_states = State_Field.__table__.delete()
        delete_chains = Chain_Field.__table__.delete()
        db.session.execute(delete_reports)
        db.session.execute(delete_years)
        db.session.execute(delete_states)
        db.session.execute(delete_chains)
        db.session.commit()
        return send_file('static/data/custom.csv',as_attachment=True)
    else:
        return '<h1>ERROR</h1>'


@app.route('/f/<string:id>')
def facility(id):
    stmt = select(Fac_Info_Field) \
            .where(Fac_Info_Field.prvdr_ccn == id) \
            .order_by(desc(Fac_Info_Field.rpt_year))
    facility = db.session.scalars(stmt).first()
    return render_template('facility.html',facility=facility)

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