import psycopg2
import pandas as pd
import numpy as np

def get_data():
    conn = psycopg2.connect(host = 'localhost', port = 5432, dbname = 'city4age', user = 'city4age_dba', password = 'city4age_dba')
    sql = '''
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
    # where risk_status in ('W', 'A')
    cur = conn.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [item[0] for item in cur.description]
    return df

def prepare_data(data):
    # print (np.unique(data['gef_name']))
    risk_mapping = {'A': 2, 'W':1, 'N': 0}
    nui_name_mapping = {label : idx for idx, label in enumerate(np.unique(data['nui_name']))}
    data['nui_name'] = data['nui_name'].map(nui_name_mapping)
    data['risk_status'] = data['risk_status'].map(risk_mapping)
    data = data[['user_in_role_id', 'gef_name', 'gef_value', 'gef_difference', 'nui_name', 'nui_value', 'nui_difference', 'risk_status', 'data_validity_status']]
    return data

