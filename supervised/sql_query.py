query0 = '''
create extension tablefunc
with schema city4age_sr
'''

query1 = '''
select
    sum(cinema_time) as cinema_time_sum,
    sum(cinema_visits) as cinema_visits_sum,
    avg(case when home_time < 86400 then home_time else NULL end) as home_time_avg,
    stddev(case when home_time < 86400 then home_time else NULL end) as home_time_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then home_time else NULL end ) as home_time_median,
    percentile_cont(0.25) within group ( order by case when home_time < 86400 then home_time else NULL end ) as home_time_best,
    avg(case when home_time < 86400 then othersocial_time else NULL end) as othersocial_time_avg,
    stddev(case when home_time < 86400 then othersocial_time else NULL end) as othersocial_time_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then othersocial_time else NULL end ) as othersocial_time_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then othersocial_time else NULL end ) as othersocial_time_best,
    avg(case when home_time < 86400 then othersocial_visits else NULL end) as othersocial_visits_avg,
    stddev(case when home_time < 86400 then othersocial_visits else NULL end) as othersocial_visits_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then othersocial_visits else NULL end ) as othersocial_visits_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then othersocial_visits else NULL end ) as othersocial_visits_best,
    sum(pharmacy_time) as pharmacy_time_sum,
    sum(pharmacy_visits) as pharmacy_visits_sum,
    sum(restaurants_time) as restaurants_time_sum,
    sum(restaurants_visits_week) as restaurants_visits_week_sum,
    avg(case when home_time < 86400 then seniorcenter_time else NULL end) as seniorcenter_time_avg,
    stddev(case when home_time < 86400 then seniorcenter_time else NULL end) as seniorcenter_time_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then seniorcenter_time else NULL end ) as seniorcenter_time_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then seniorcenter_time else NULL end ) as seniorcenter_time_best,
    avg(case when home_time < 86400 then seniorcenter_visits else NULL end) as seniorcenter_visits_avg,
    stddev(case when home_time < 86400 then seniorcenter_visits else NULL end) as seniorcenter_visits_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then seniorcenter_visits else NULL end ) as seniorcenter_visits_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then seniorcenter_visits else NULL end ) as seniorcenter_visits_best,
    avg(case when home_time < 86400 then shops_outdoor_time_perc else NULL end) as shops_outdoor_time_perc_avg,
    stddev(case when home_time < 86400 then shops_outdoor_time_perc else NULL end) as shops_outdoor_time_perc_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then shops_outdoor_time_perc else NULL end ) as shops_outdoor_time_perc_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then shops_outdoor_time_perc else NULL end ) as shops_outdoor_time_perc_best,
    avg(case when home_time < 86400 then shops_time else NULL end) as shops_time_avg,
    stddev(case when home_time < 86400 then shops_time else NULL end) as shops_time_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then shops_time else NULL end ) as shops_time_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then shops_time else NULL end ) as shops_time_best,
    avg(case when home_time < 86400 then shops_visits else NULL end) as shops_visits_avg,
    stddev(case when home_time < 86400 then shops_visits else NULL end) as shops_visits_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then shops_visits else NULL end ) as shops_visits_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then shops_visits else NULL end ) as shops_visits_best,
    avg(case when home_time < 86400 then transport_time else NULL end) as transport_time_avg,
    stddev(case when home_time < 86400 then transport_time else NULL end) as transport_time_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then transport_time else NULL end ) as transport_time_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then transport_time else NULL end ) as transport_time_best,
    avg(case when home_time < 86400 then walk_distance_outdoor else NULL end) as walk_distance_outdoor_avg,
    stddev(case when home_time < 86400 then walk_distance_outdoor else NULL end) as walk_distance_outdoor_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then walk_distance_outdoor else NULL end ) as walk_distance_outdoor_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then walk_distance_outdoor else NULL end ) as walk_distance_outdoor_best,
    avg(case when home_time < 86400 then walk_speed_outdoor else NULL end) as walk_speed_outdoor_avg,
    stddev(case when home_time < 86400 then walk_speed_outdoor else NULL end) as walk_speed_outdoor_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then walk_speed_outdoor else NULL end ) as walk_speed_outdoor_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then walk_speed_outdoor else NULL end ) as walk_speed_outdoor_best,
    avg(case when home_time < 86400 then walk_time_outdoor else NULL end) as walk_time_outdoor_avg,
    stddev(case when home_time < 86400 then walk_time_outdoor else NULL end) as walk_time_outdoor_sd,
    percentile_cont(0.5) within group ( order by case when home_time < 86400 then walk_time_outdoor else NULL end ) as walk_time_outdoor_median,
    percentile_cont(0.75) within group ( order by case when home_time < 86400 then walk_time_outdoor else NULL end ) as walk_time_outdoor_best,
    status
from city4age_sr.crosstab('
    select format(''%s%s'', date(time_interval.interval_start), care_recipient.id) as row_name, case when time_interval.interval_start <= ''2018-01-31'' then 1 else 2 end as trimester, date(time_interval.interval_start), care_recipient.id, variable.detection_variable_name, measure.measure_value
    from
        city4age_sr.variation_measure_value as measure inner join
        city4age_sr.user_in_role as care_recipient on measure.user_in_role_id = care_recipient.id inner join
        city4age_sr.pilot as pilot on care_recipient.pilot_code = pilot.pilot_code inner join
        city4age_sr.cd_detection_variable as variable on measure.measure_type_id = variable.id inner join
        city4age_sr.time_interval as time_interval on measure.time_interval_id = time_interval.id
    where
        pilot.pilot_code = ''ath'' and
        date(time_interval.interval_start) >= ''2017-11-10'' and date(time_interval.interval_start) <= ''2018-04-30''
    order by 1
    ','
    select cat 
    from (VALUES
        (''cinema_time''),
        (''cinema_visits''),
        (''cinema_visits_month''),
        (''home_time''),
        (''othersocial_time''),
        (''othersocial_visits''),
        (''pharmacy_time''),
        (''pharmacy_visits''),
        (''pharmacy_visits_month''),
        (''restaurants_time''),
        (''restaurants_visits_week''),
        (''seniorcenter_time''),
        (''seniorcenter_visits''),
        (''shops_outdoor_time_perc''),
        (''shops_time''),
        (''shops_visits''),
        (''supermarket_time''),
        (''supermarket_visits''),
        (''transport_time''),
        (''walk_distance_outdoor''),
        (''walk_distance_outdoor_fast_perc''),
        (''walk_distance_outdoor_slow_perc''),
        (''walk_speed_outdoor''),
        (''walk_time_outdoor'')) as v(cat)
    order by 1
    ') as ct(
        row_name text,
        trimester numeric,
        day_m date,
        cr_m numeric,
        cinema_time numeric,
        cinema_visits numeric,
        cinema_visits_month numeric,
        home_time numeric,
        othersocial_time numeric,
        othersocial_visits numeric,
        pharmacy_time numeric,
        pharmacy_visits numeric,
        pharmacy_visits_month numeric,
        restaurants_time numeric,
        restaurants_visits_week numeric,
        seniorcenter_time numeric,
        seniorcenter_visits numeric,
        shops_outdoor_time_perc numeric,
        shops_time numeric,
        shops_visits numeric,
        supermarket_time numeric,
        supermarket_visits numeric,
        transport_time numeric,
        walk_distance_outdoor numeric,
        walk_distance_outdoor_fast_perc numeric,
        walk_distance_outdoor_slow_perc numeric,
        walk_speed_outdoor numeric,
        walk_time_outdoor numeric
    ) inner join (VALUES
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
    ) as labels(cr_m, trimester, status)
    on ct.cr_m = labels.cr_m and ct.trimester = labels.trimester
group by ct.cr_m, ct.trimester, status
having count(case when home_time < 86400 then 1 end) > 10
order by 1,2
'''