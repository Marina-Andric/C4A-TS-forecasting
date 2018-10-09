import psycopg2
import pandas as pd
import numpy as np
import datetime

def get_data(host_name, username, password):
    conn = psycopg2.connect(host = host_name, port = 5432, dbname = 'city4age', user = username, password = password)
    sql_old = '''
    with q0 as
 (
  select
   uir.id as user_in_role_id ,
   ti.id  as time_interval_id,
   ti.interval_start         ,
   gef.gef_type_id           ,
   gef.gef_value             ,
   nui.nui_type_id           ,
   nui.nui_value
  from
   city4age_sr.geriatric_factor_value as gef
   join
    city4age_sr.user_in_role as uir
    on
     gef.user_in_role_id = uir.id
   join
    city4age_sr.md_pilot_detection_variable as pdv
    on
     gef.gef_type_id    = pdv.derived_detection_variable_id
     and uir.pilot_code = pdv.pilot_code
   join
    city4age_sr.numeric_indicator_value as nui
    on
     gef.time_interval_id    = nui.time_interval_id
     and gef.user_in_role_id = nui.user_in_role_id
     and nui.nui_type_id     = pdv.detection_variable_id
   join
    city4age_sr.time_interval as ti
    on
     gef.time_interval_id = ti.id
 )
 ,
 q1 as
 (
  select
   gef.user_in_role_id                   ,
   ti.id as time_interval_id             ,
   ti.interval_start                     ,
   dv.detection_variable_name as gef_name,
   gef.gef_value                         ,
   gef_type_id                           ,
   -- nui.nui_type_id,
   dv1.detection_variable_name as nui_name,
   nui.nui_value                          ,
   nui.nui_type_id                        ,
   assessment.risk_status                 ,
   assessment.data_validity_status        ,
   assessment.assessment_comment
  from
   city4age_sr.assessment
   join
    city4age_sr.assessed_gef_value_set as agef
    on
     assessment.id = agef.assessment_id
   join
    city4age_sr.geriatric_factor_value as gef
    on
     agef.gef_value_id = gef.id
   join
    city4age_sr.cd_detection_variable as dv
    on
     gef.gef_type_id = dv.id
   join
    city4age_sr.user_in_role as uir
    on
     gef.user_in_role_id = uir.id
   join
    city4age_sr.md_pilot_detection_variable as pdv
    on
     gef.gef_type_id    = pdv.derived_detection_variable_id
     and uir.pilot_code = pdv.pilot_code
   join
    city4age_sr.numeric_indicator_value as nui
    on
     nui.user_in_role_id           = gef.user_in_role_id
     and gef.time_interval_id      = nui.time_interval_id
     and pdv.detection_variable_id = nui.nui_type_id
   join
    city4age_sr.cd_detection_variable as dv1
    on
     dv1.id = nui_type_id
   join
    city4age_sr.time_interval as ti
    on
     gef.time_interval_id = ti.id
  order by
   gef.user_in_role_id
 )
 ,
 gef_dif as
 (
  select DISTINCT
   tab1.user_in_role_id                      ,
   tab1.gef_type_id                          ,
   tab1.time_interval_id                     ,
   tab1.interval_start                       ,
   tab2.interval_start as interval_start_prev,
   tab1.gef_value                            ,
   tab2.gef_value as gef_value_prev
  from
   q1 as tab1
   join
    q0 as tab2
    on
     tab1.user_in_role_id = tab2.user_in_role_id
     and tab1.gef_type_id = tab2.gef_type_id
  where
   tab2.interval_start = tab1.interval_start - interval '1 month'
 )
 ,
 nui_dif as
 (
  select
   tab1.user_in_role_id                      ,
   tab1.nui_type_id                          ,
   tab1.time_interval_id                     ,
   tab1.interval_start                       ,
   tab1.nui_name                             ,
   tab2.interval_start as interval_start_prev,
   tab1.nui_value                            ,
   tab2.nui_value as nui_value_prev
  from
   q1 as tab1
   join
    q0 as tab2
    on
     tab1.user_in_role_id = tab2.user_in_role_id
     and tab1.gef_type_id = tab2.gef_type_id
     and tab1.nui_type_id = tab2.nui_type_id
  where
   tab2.interval_start = tab1.interval_start - interval '1 month'
 )
-- select *
-- from q1
-- order by nui_name
select distinct
 q1.user_in_role_id                                         ,
 q1.interval_start                                          ,
 q1.gef_name                                                ,
 q1.gef_value                                               ,
 gef_dif.gef_value - gef_dif.gef_value_prev as gef_difference,
 q1.nui_name                                                ,
 q1.nui_value                                               ,
 nui_dif.nui_value - nui_dif.nui_value_prev as nui_difference,
 q1.risk_status                                             ,
 q1.data_validity_status                                    ,
 q1.assessment_comment
from
 q1
 join
  gef_dif
  on
   q1.user_in_role_id      = gef_dif.user_in_role_id
   and q1.gef_type_id      = gef_dif.gef_type_id
   and q1.time_interval_id = gef_dif.time_interval_id
 join
  nui_dif
  on
   q1.user_in_role_id      = nui_dif.user_in_role_id
   and q1.nui_type_id      = nui_dif.nui_type_id
   and q1.time_interval_id = nui_dif.time_interval_id   
   where data_validity_status = 'V' and q1.nui_name like '%avg%'
    '''
    sql = '''
WITH q0_gef AS (
        SELECT
            uir. ID AS user_in_role_id,
            ti. ID AS time_interval_id,
            ti.interval_start,
            ti."id" AS timeid,
            gef.gef_type_id,
            gef.gef_value,
            nui.nui_type_id,
            nui.nui_value
        FROM
            city4age_sr.geriatric_factor_value AS gef
        JOIN city4age_sr.user_in_role AS uir ON gef.user_in_role_id = uir. ID
        JOIN city4age_sr.md_pilot_detection_variable AS pdv ON gef.gef_type_id = pdv.derived_detection_variable_id
        AND uir.pilot_code = pdv.pilot_code
        JOIN city4age_sr.md_pilot_detection_variable AS pdv1 ON pdv.detection_variable_id = pdv1.derived_detection_variable_id
        AND uir.pilot_code = pdv1.pilot_code
        JOIN city4age_sr.numeric_indicator_value AS nui ON gef.time_interval_id = nui.time_interval_id
        AND gef.user_in_role_id = nui.user_in_role_id
        AND nui.nui_type_id = pdv1.detection_variable_id
        JOIN city4age_sr.time_interval AS ti ON gef.time_interval_id = ti. ID
    ),
     q0_ges AS (
        SELECT
            uir. ID AS user_in_role_id,
            ti. ID AS time_interval_id,
            ti.interval_start,
            ti."id" AS timeid,
            gef.gef_type_id,
            gef.gef_value,
            nui.nui_type_id,
            nui.nui_value
        FROM
            city4age_sr.geriatric_factor_value AS gef
        JOIN city4age_sr.user_in_role AS uir ON gef.user_in_role_id = uir. ID
        JOIN city4age_sr.md_pilot_detection_variable AS pdv ON gef.gef_type_id = pdv.derived_detection_variable_id
        AND uir.pilot_code = pdv.pilot_code
        JOIN city4age_sr.numeric_indicator_value AS nui ON gef.time_interval_id = nui.time_interval_id
        AND gef.user_in_role_id = nui.user_in_role_id
        AND nui.nui_type_id = pdv.detection_variable_id
        JOIN city4age_sr.time_interval AS ti ON gef.time_interval_id = ti. ID
    ),
     q0 AS (
        SELECT
            *
        FROM
            q0_gef
        UNION
            SELECT
                *
            FROM
                q0_ges
    ),
     q1_gef AS (
        SELECT
            gef.user_in_role_id,
            ti. ID AS time_interval_id,
            ti.interval_start,
            dv.detection_variable_name AS gef_name,
            gef.gef_value,
            gef_type_id,
            -- nui.nui_type_id,
            dv2.detection_variable_name AS nui_name,
            nui.nui_value,
            nui.nui_type_id,
            -- nui.id as nuiid,
            assessment.risk_status,
            assessment.data_validity_status,
            assessment.assessment_comment
        FROM
            city4age_sr.assessment
        JOIN city4age_sr.assessed_gef_value_set AS agef ON assessment. ID = agef.assessment_id
        JOIN city4age_sr.geriatric_factor_value AS gef ON agef.gef_value_id = gef. ID
        JOIN city4age_sr.cd_detection_variable AS dv ON gef.gef_type_id = dv. ID
        JOIN city4age_sr.user_in_role AS uir ON gef.user_in_role_id = uir. ID
        JOIN city4age_sr.md_pilot_detection_variable AS pdv ON gef.gef_type_id = pdv.derived_detection_variable_id
        AND uir.pilot_code = pdv.pilot_code
        JOIN city4age_sr.cd_detection_variable dv1 ON pdv.detection_variable_id = dv1. ID -- and pdv.detection_variable_type <> 'mea'
        LEFT JOIN city4age_sr.md_pilot_detection_variable AS pdv1 ON pdv.detection_variable_id = pdv1.derived_detection_variable_id
        AND uir.pilot_code = pdv1.pilot_code
        INNER JOIN city4age_sr.cd_detection_variable dv2 ON dv2. ID = pdv1.detection_variable_id
        AND dv2.detection_variable_type = 'nui'
        JOIN city4age_sr.numeric_indicator_value AS nui ON nui.user_in_role_id = gef.user_in_role_id
        AND gef.time_interval_id = nui.time_interval_id
        AND pdv1.detection_variable_id = nui.nui_type_id -- 	OR pdv1.detection_variable_id = nui.nui_type_id
        JOIN city4age_sr.cd_detection_variable AS dv3 ON dv3. ID = nui_type_id
        JOIN city4age_sr.time_interval AS ti ON gef.time_interval_id = ti. ID
        WHERE
            gef.user_in_role_id > 100 --  and dv.detection_variable_name = 'physical_activity'
        ORDER BY
            gef.user_in_role_id
    ),
     q1_ges AS (
        SELECT
            gef.user_in_role_id,
            ti. ID AS time_interval_id,
            ti.interval_start,
            dv.detection_variable_name AS gef_name,
            gef.gef_value,
            gef_type_id,
            -- nui.nui_type_id,
            dv1.detection_variable_name AS nui_name,
            nui.nui_value,
            nui.nui_type_id,
            -- nui.id as nuiid,
            assessment.risk_status,
            assessment.data_validity_status,
            assessment.assessment_comment
        FROM
            city4age_sr.assessment
        JOIN city4age_sr.assessed_gef_value_set AS agef ON assessment. ID = agef.assessment_id
        JOIN city4age_sr.geriatric_factor_value AS gef ON agef.gef_value_id = gef. ID
        JOIN city4age_sr.cd_detection_variable AS dv ON gef.gef_type_id = dv. ID
        JOIN city4age_sr.user_in_role AS uir ON gef.user_in_role_id = uir. ID
        JOIN city4age_sr.md_pilot_detection_variable AS pdv ON gef.gef_type_id = pdv.derived_detection_variable_id
        AND uir.pilot_code = pdv.pilot_code -- 	join cd_detection_variable dv1 on pdv.detection_variable_id = dv1.id 
        -- and pdv.detection_variable_type <> 'mea'
        JOIN city4age_sr.numeric_indicator_value AS nui ON nui.user_in_role_id = gef.user_in_role_id
        AND gef.time_interval_id = nui.time_interval_id
        AND pdv.detection_variable_id = nui.nui_type_id
        JOIN city4age_sr.cd_detection_variable AS dv1 ON dv1. ID = nui_type_id
        JOIN city4age_sr.time_interval AS ti ON gef.time_interval_id = ti. ID
        WHERE
            gef.user_in_role_id > 100 --  and dv.detection_variable_name = 'physical_activity'
        ORDER BY
            gef.user_in_role_id
    ),
     q1 AS (
        SELECT
            *
        FROM
            q1_gef
        UNION
            SELECT
                *
            FROM
                q1_ges
    ),
     gef_dif AS (
        SELECT DISTINCT
            tab1.user_in_role_id,
            tab1.gef_type_id,
            tab1.time_interval_id,
            tab1.interval_start,
            tab2.interval_start AS interval_start_prev,
            tab1.gef_value,
            tab2.gef_value AS gef_value_prev
        FROM
            q1 AS tab1
        JOIN q0_gef AS tab2 ON tab1.user_in_role_id = tab2.user_in_role_id
        AND tab1.gef_type_id = tab2.gef_type_id
        WHERE
            tab2.interval_start = tab1.interval_start - INTERVAL '1 month'
    ),
     nui_dif AS (
        SELECT
            tab1.user_in_role_id,
            tab1.nui_type_id,
            tab2.gef_type_id,
            tab1.time_interval_id,
            tab1.interval_start,
            tab1.nui_name,
            tab2.interval_start AS interval_start_prev,
            tab1.nui_value,
            tab2.nui_value AS nui_value_prev
        FROM
            q1 AS tab1
        JOIN q0_gef AS tab2 ON tab1.user_in_role_id = tab2.user_in_role_id
        AND tab1.gef_type_id = tab2.gef_type_id
        AND tab1.nui_type_id = tab2.nui_type_id
        WHERE
            tab2.interval_start = tab1.interval_start - INTERVAL '1 month'
    )SELECT DISTINCT
        q1.user_in_role_id,
        q1.interval_start,
        -- 	q1.time_interval_id,
        q1.gef_name,
        q1.gef_value,
        gef_dif.gef_value - gef_dif.gef_value_prev AS gef_difference,
        q1.nui_name,
        q1.nui_value,
        -- 	q1.nui_type_id,
        nui_dif.nui_value - nui_dif.nui_value_prev AS nui_difference,
       -- q1.risk_status,
        CASE
        WHEN q1.user_in_role_id = 129
        AND q1.gef_value = 1.5 
          THEN
            'A'
        ELSE
            q1.risk_status
        END AS risk_status,
     q1.data_validity_status,
     q1.assessment_comment
    FROM
        q1
    JOIN gef_dif ON q1.user_in_role_id = gef_dif.user_in_role_id
    AND q1.gef_type_id = gef_dif.gef_type_id
    AND q1.time_interval_id = gef_dif.time_interval_id
    JOIN nui_dif ON q1.user_in_role_id = nui_dif.user_in_role_id
    AND q1.time_interval_id = nui_dif.time_interval_id
    AND nui_dif.gef_type_id = q1.gef_type_id
    AND q1.nui_type_id = nui_dif.nui_type_id
    WHERE
        (
            q1.gef_name = 'motility'
            OR q1.gef_name = 'walking'
        )
    AND q1.assessment_comment NOT LIKE '%August%'
    AND q1.assessment_comment NOT LIKE '%august%'
    AND q1.assessment_comment LIKE '% %'
    AND q1.assessment_comment NOT LIKE '%Compared to previous month the number of steps increased whereas distance dropped%'
    AND q1.assessment_comment NOT LIKE '%Values in July 2018 plummeted%'
    AND q1.assessment_comment NOT LIKE '%Compared to February 2018 both walking steps and distance rose%'
    AND q1.assessment_comment NOT LIKE '%Compared to February 2018 values rose consistently%'
    AND q1.assessment_comment NOT LIKE '%Slight increase in both steps and distance compared to April 2018%'
    AND q1.assessment_comment NOT LIKE '%In July 2018 sharp drop in values%'
    AND q1.assessment_comment NOT LIKE '%Compared to previous month soft activity slightly increased with a sharp decrease in both moderate and intense activity%'
    AND q1.assessment_comment NOT LIKE '%Sharp reduction in walking steps and distance for July 2018%'
    AND q1.assessment_comment NOT LIKE '%Values went down in July 2018%'
    AND q1.assessment_comment NOT LIKE '%only four%'
    AND q1.assessment_comment NOT LIKE '%Discuss with geriatrician%'
--    and not(q1.assessment_comment like '%Compared to previous month sharp drop in both steps and distance%' and q1.user_in_role_id = 129)
    ORDER BY
        nui_value
    '''
    # where risk_status in ('W', 'A')
    cur = conn.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [item[0] for item in cur.description]
    # df.to_csv('Images/output.csv')
    return df

def prepare_data(data):
    data = data[data['data_validity_status']=='V']
    risk_mapping = {'A': 2, 'W':1, 'N': 0}
    nui_name_mapping = {label : idx for idx, label in enumerate(np.unique(data['nui_name']))}
    # data['nui_name'] = data['nui_name'].map(nui_name_mapping)
    data['risk_status'] = data['risk_status'].map(risk_mapping)
    data['interval_start'] = [datum.strftime('%Y-%m-%d') for datum in data['interval_start']]
    data['interval_start'] = [datetime.datetime.strptime(datum, '%Y-%m-%d') for datum in data['interval_start']]
    data = data[['user_in_role_id', 'interval_start', 'gef_name', 'gef_value', 'gef_difference', 'nui_name', 'nui_value', 'nui_difference', 'risk_status', 'data_validity_status']]
    return data

def get_motility_data(data):
    motility_data = data[(data['gef_name']=='motility') | (data['gef_name']=='walking')]
    motility_data = pd.pivot_table(motility_data, index =['interval_start', 'user_in_role_id', 'risk_status', 'gef_value', 'gef_difference'],
                                   columns = 'nui_name', values= ['nui_value', 'nui_difference'], aggfunc= np.max)
    motility_data.columns = [f'{j}_{i}' for i, j in motility_data.columns]
    motility_data = motility_data.reset_index()
    motility_data=motility_data.sort_values('risk_status')
    motility_data.reset_index(drop= True, inplace=True)
    motility_data = motility_data.iloc[:,2:]
    # motility_data.to_csv('Images/output.csv')
    # print (motility_data)
    return motility_data


