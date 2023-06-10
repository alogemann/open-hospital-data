from app_package import db

class Report_field(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    var_name = db.Column(db.String(20), nullable = False)
    wksht_cd = db.Column(db.String(7), nullable = False)
    line_num = db.Column(db.String(5), nullable = False)
    clmn_num = db.Column(db.String(5), nullable = False)

    def __repr__(self):
        return f"Report_field('{self.var_name}','{self.wksht_cd}','{self.line_num}','{self.clmn_num}')"
        