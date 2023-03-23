import sqlite3 as sql
from flask import Flask, render_template, redirect, send_file, url_for, flash
from forms import ClearForm, FieldsForm, CreateForm
from helpers import format_field
from sql_helpers import load_data, make_data
from keys import CONNECTION_STRING, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

FIELDS = {}

@app.get('/')
@app.get('/index')
def index():
    return render_template('index.html')

@app.route('/custom', methods=['GET','POST'])
def custom():

    global FIELDS

    fields_form = FieldsForm()
    clear_form = ClearForm()
    create_form = CreateForm()

    if fields_form.validate_on_submit():
        new_var = {'wksht_cd': 'S200001',
                    'line_num': format_field(fields_form.line_number.data),
                    'clmn_num': format_field(fields_form.column_number.data)}

        if len(fields_form.var_name.data) > 0:
            FIELDS[fields_form.var_name.data] = new_var
        else:
            FIELDS[f'Variable-{len(FIELDS)+1}'] = new_var
        return redirect(url_for('custom'))
    
    elif create_form.validate_on_submit():
        flash('Your dataset is being created.')
        con = sql.connect('cost_reports.db')
        base_df = load_data(FIELDS,con)
        new_df = make_data(base_df,FIELDS,con)
        new_df.to_csv('static/data.csv', index=False)
        con.close()
        return send_file('static/data.csv', as_attachment=True)  
    
    elif clear_form.validate_on_submit():
        FIELDS = {}
        return redirect(url_for('custom'))
    
    else:
        return render_template('custom.html', fields_form = fields_form, clear_form = clear_form, create_form = create_form, fields=FIELDS)


if __name__ == '__main__':
    app.run(debug=True)
