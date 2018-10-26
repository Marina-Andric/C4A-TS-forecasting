
query1 = '''
select ct.cr_id, ct.var_name, ct.trimester, ct.day_m, ct.val, labels.status from 
(select 
care_recipient.id as cr_id, 
variable.detection_variable_name as var_name, 
case when time_interval.interval_start <= '2018-01-31' then 1 else 2 end as trimester, 
date(time_interval.interval_start) as day_m, 
measure.measure_value as val
    from
        city4age_sr.variation_measure_value as measure inner join
        city4age_sr.user_in_role as care_recipient on measure.user_in_role_id = care_recipient.id inner join
        city4age_sr.pilot as pilot on care_recipient.pilot_code = pilot.pilot_code inner join
        city4age_sr.cd_detection_variable as variable on measure.measure_type_id = variable.id inner join
        city4age_sr.time_interval as time_interval on measure.time_interval_id = time_interval.id
    where
        pilot.pilot_code = 'ath' and
        date(time_interval.interval_start) >= '2017-11-10' and date(time_interval.interval_start) <= '2018-04-30'
    order by day_m) as ct
inner join (VALUES
        (10, 1, 'Robust'),
        (11, 1, 'preFrail'),
        (12, 1, 'Robust'),
        (13, 1, 'preFrail'),
        (14, 1, 'Robust'),
        (15, 1, 'Robust'),
        (16, 1, 'Frail'),
        (17, 1, 'Frail'),
        (18, 1, 'preFrail'),
        (19, 1, 'Robust'),
        (20, 1, 'Robust'),
        (21, 1, 'Robust'),
        (22, 1, 'Robust'),
        (23, 1, 'preFrail'),
        (24, 1, 'preFrail'),
        (25, 1, 'postRrobust'),
        (26, 1, 'Robust'),
        (27, 1, 'Robust'),
        (28, 1, 'Robust'),
        (29, 1, 'preFrail'),
        (30, 1, 'Frail'),
        (32, 1, 'Robust'),
        (33, 1, 'Robust'),
        (34, 1, 'postRrobust'),
        (35, 1, 'Robust'),
        (36, 1, 'Robust'),
        (37, 1, 'Robust'),
        (38, 1, 'Frail'),
        (39, 1, 'postRrobust'),
        (40, 1, 'Robust'),
        (41, 1, 'Robust'),
        (42, 1, 'preFrail'),
        (43, 1, 'preFrail'),
        (44, 1, 'Robust'),
        (45, 1, 'Robust'),
        (49, 1, 'Robust'),
        (50, 1, 'Robust'),
        (58, 1, 'Robust'),
        (168,1, 'Robust'),
        (169,1, 'Robust'),
        (10, 2, 'Frail'),
        (11, 2, 'preFrail'),
        (12, 2, 'Robust'),
        (13, 2, 'preFrail'),
        (14, 2, 'preFrail'),
        (15, 2, 'preFrail'),
        (16, 2, 'Frail'),
        (17, 2, 'Robust'),
        (18, 2, 'Robust'),
        (19, 2, 'Robust'),
        (20, 2, 'preFrail'),
        (21, 2, 'Robust'),
        (22, 2, 'preFrail'),
        (23, 2, 'preFrail'),
        (24, 2, 'preFrail'),
        (25, 2, 'preFrail'),
        (26, 2, 'Robust'),
        (27, 2, 'Robust'),
        (28, 2, 'Robust'),
        (29, 2, 'Robust'),
        (30, 2, 'postRrobust'),
        (32, 2, 'Robust'),
        (33, 2, 'Robust'),
        (34, 2, 'Frail'),
        (35, 2, 'Robust'),
        (36, 2, 'preFrail'),
        (37, 2, 'preFrail'),
        (38, 2, 'Frail'),
        (39, 2, 'postRrobust'),
        (40, 2, 'preFrail'),
        (41, 2, 'Robust'),
        (42, 2, 'preFrail'),
        (43, 2, 'preFrail'),
        (44, 2, 'Robust'),
        (45, 2, 'preFrail'),
        (49, 2, 'preFrail'),
        (49, 2, 'Robust'),
        (50, 2, 'Robust'),
        (58, 2, 'preFrail'),
        (168,2, 'Robust'),
        (169,2, 'preFrail')
    ) as labels(cr_id, trimester, status)
    on ct.cr_id = labels.cr_id and ct.trimester = labels.trimester
'''