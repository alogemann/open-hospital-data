import pandas as pd

def load_data(data, con):
    cur = con.cursor()
    for key, value in data.items():
        cur.execute(f"""
            create table {key} as
            select rpt_rec_num, itm_txt
            from rpt_data_long 
            where wksht_cd = '{value['wksht_cd']}' 
                and line_num = '{value['line_num']}' 
                and clmn_num = '{value['clmn_num']}'
            """)
    cur.execute(f'select rpt_rec_num from {list(data.keys())[0]}')
    return pd.DataFrame(cur.fetchall(), columns=['rpt_rec_num'])

def make_data(base_df, data, con):
    cur = con.cursor()
    for key in data:
        cur.execute(f'select * from {key}')
        new_df = pd.DataFrame(cur.fetchall(), columns=['rpt_rec_num',key])
        base_df = base_df.merge(new_df)
        cur.execute(f'drop table {key}')
    return base_df

