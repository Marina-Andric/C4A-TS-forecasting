import psycopg2 as pg
import json

conn=pg.connect("host=localhost port=5432 user=city4age_dba password=city4age_dba dbname=city4age")
# conn=pg.connect("host=109.111.225.84 port=5432 user=city4age_srv password=city4age_srv dbname=city4age")
cur_read = conn.cursor()
cur_write = conn.cursor()

with open("Data//assessment_backup.json") as f:
    podaci = json.load(f)

for k, v in podaci.items():
    k2 = tuple(map(int, k.split("-")))
    print(k2)
    # trenutne vrednosti, privremeno resenje!!!
    if k2[1] == 12120:
        ti_id = 11155
    elif k2[1] == 10871:
        ti_id = 10061
    elif k2[1] == 12119:
        ti_id = 8590
    else:
        ti_id = k2[1]
    cur_read.execute('SELECT gfv."id" FROM city4age_sr.geriatric_factor_value gfv WHERE gfv.user_in_role_id = %s AND gfv.time_interval_id = %s AND gfv.gef_type_id = %s;', (k2[0], ti_id, k2[2]))
    row = cur_read.fetchone()
    print(row)
    print("")
    if row:
        for ass_id in v:
            cur_write.execute('INSERT INTO city4age_sr.assessed_gef_value_set (gef_value_id, assessment_id) VALUES (%s, %s);', (row[0], ass_id))

cur_read.close()
cur_write.close()
conn.commit()