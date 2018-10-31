import psycopg2 as pg
import json

conn=pg.connect("host=localhost port=5432 user=city4age_dba password=city4age_dba dbname=city4age")
cur=conn.cursor()

cur.execute('SELECT ass.assessment_id, gfv."id", gfv.user_in_role_id, gfv.time_interval_id, gfv.gef_type_id FROM city4age_sr.geriatric_factor_value gfv INNER JOIN city4age_sr.assessed_gef_value_set ass on gfv."id" = ass.gef_value_id;')

podaci = {}

row = cur.fetchone()

while row:
    assessment_id, old_id, user_in_role_id, time_interval_id, gef_type_id = row
    key = '%i-%i-%i' % (user_in_role_id, time_interval_id, gef_type_id)
    if not key in podaci:
        podaci[key] = []
    podaci[key].append(assessment_id)
    row = cur.fetchone()

with open("assessment_backup.json", "w") as f:
    json.dump(podaci, f)
