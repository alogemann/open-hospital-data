import pandas as pd
from flask import render_template, redirect, send_file, url_for, request
from sqlalchemy import text
from app_package import app, db
from app_package.forms import ClearForm, FieldsForm, CreateForm, DownloadForm
from app_package.models import Report_field
from app_package.helpers import format_field

@app.get('/')
@app.get('/index')
def index():
    return render_template('index.html')

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

    ##Post Request
    if fields_form.validate_on_submit():
        new_field = Report_field(var_name = fields_form.var_name.data,
                                    wksht_cd = fields_form.worksheet.data,
                                    line_num = fields_form.line_number.data,
                                    clmn_num = fields_form.column_number.data)
        db.session.add(new_field)
        db.session.commit()
        return redirect(url_for('custom'))
    
    elif clear_form.validate_on_submit():
        delete_fields = Report_field.__table__.delete()
        db.session.execute(delete_fields)
        db.session.commit()
        return redirect(url_for('custom'))
    
    elif create_form.validate_on_submit():
        db.session.execute(text('CALL build_variables();'))
        db.session.commit()
        db.session.execute(text('CALL build_table();'))
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
        new_df = pd.DataFrame(db.session.execute(text('Select * from new_table')))
        new_df.to_csv('app_package/static/custom.csv',index=False)
        #db.session.execute(text('CALL drop tables();'))
        #db.session.commit()
        delete_fields = Report_field.__table__.delete()
        db.session.execute(delete_fields)
        db.session.commit()
        return send_file('static/custom.csv',as_attachment=True)
    else:
        return '<h1>ERROR</h1>'
