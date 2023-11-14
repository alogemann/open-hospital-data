from app_package import db

class Report_field(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    var_name = db.Column(db.String(40), nullable = False)
    wksht_cd = db.Column(db.String(7), nullable = False)
    line_num = db.Column(db.String(5), nullable = False)
    clmn_num = db.Column(db.String(5), nullable = False)

    def __repr__(self):
        return f"Report_field('{self.var_name}','{self.wksht_cd}','{self.line_num}','{self.clmn_num}')"

class Field_presets(db.Model):
    __table_args__ = {"schema":"renal"}

    id = db.Column(db.Integer, primary_key=True)
    var_name = db.Column(db.String(40), nullable = False)
    wksht_cd = db.Column(db.String(7), nullable = False)
    line_num = db.Column(db.String(5), nullable = False)
    clmn_num = db.Column(db.String(5), nullable = False)

    def __repr__(self):
        return f"Field_presets('{self.var_name}','{self.wksht_cd}','{self.line_num}','{self.clmn_num}')"


class Fac_Info_Field(db.Model):
    __tablename__ = 'facility_info'
    __table_args__ = {"schema":"renal"}

    rpt_rec_num = db.Column(db.Integer, primary_key=True)
    prvdr_ccn = db.Column(db.String(40), nullable = False)
    prvdr_name = db.Column(db.String(40))
    prvdr_addr = db.Column(db.String(40))
    prvdr_city = db.Column(db.String(40))
    prvdr_county = db.Column(db.String(40))
    prvdr_zip = db.Column(db.String(40))
    prvdr_state = db.Column(db.String(40))
    prvdr_cbsa = db.Column(db.String(40))
    type_control = db.Column(db.String(40))
    chain_name = db.Column(db.String(40))
    rpt_year = db.Column(db.Integer)

    def __repr__(self):
        return f"Fac_info_field('{self.prvdr_ccn.strip()}','{self.prvdr_name.strip()}','{self.rpt_year}')"

class Year_Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable = False)
    
class State_Field(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    state = db.Column(db.String(2), nullable = False)

class Chain_Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chain = db.Column(db.String(40), nullable = False)

"""
class Worksheet_field(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    wksht_name = db.Column(db.String(7), nullable=False)

class Preset_Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preset_name = db.Column(db.String(20), nullable = False)
    preset_src = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return f"Preset_field('{self.preset_name}', '{self.preset_src}')"

"""