from scipy.stats import pearsonr
import psycopg2
import pandas as pd

def get_data(userId, gefId):
    conn = psycopg2.connect(host = 'localhost', port = 5432, database = 'city4age', user = 'city4age_dba', password = 'city4age_dba')
    sql = '''
    SELECT
        gfv1.user_in_role_id,
        gfv1.gef_type_id AS gefId,
        gfv1.gef_value AS gefVal,
        gfv2.gef_type_id,
        gfv2.gef_value
    FROM
        city4age_sr.geriatric_factor_value AS gfv1
    JOIN city4age_sr.geriatric_factor_value AS gfv2 ON gfv1.user_in_role_id = gfv2.user_in_role_id
    AND gfv1.time_interval_id = gfv2.time_interval_id
    WHERE
        gfv2.gef_type_id = 501 and not gfv1.gef_type_id = 501
    AND gfv1.user_in_role_id = {0} and gfv1.gef_type_id = {1}
    '''.format(userId, gefId)
    cur = conn.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [item[0] for item in cur.description]
    return df

data = get_data(114, 505)
# print (data)
#  504, 514, 505

x = [float(item) for item in data['gefval']]
y = [float(item) for item in data['gef_value'].tolist()]

print (x)
print (y)

corr, p_val = pearsonr(x[:4], y[:4])
print ('corr = %.2f, p_val = %.2f'% (corr, p_val))

# corr_mot, p_val = pearsonr(mot_127, ovl_127)
# print ("Motility: corr = %.2f, p_val = %.2f" % (corr_mot, p_val))
#
# corr_health, p_val = pearsonr(hphy_127, ovl_127)
# print ("Physical health: corr = %.2f, p_val = %.2f" % (corr_health, p_val))
#
# corr_activity, p_val = pearsonr(phyact_127, ovl_127)
# print ("Physical activity: corr = %.2f, p_val = %.2f" % (corr_activity, p_val))