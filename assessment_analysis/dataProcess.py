import psycopg2
import pandas as pd
import numpy as np
import datetime

def get_data(host_name, username, password):
    conn = psycopg2.connect(host = host_name, port = 5432, dbname = 'city4age', user = username, password = password)
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
        WHERE
            gef.gef_type_id IN (504, 514) -- walking or motility
        AND uir.pilot_code LIKE '%bhx%'
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
        WHERE
            gef.gef_type_id IN (504, 514) -- walking or motility
        AND uir.pilot_code LIKE '%bhx%'
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
            uir.pilot_code LIKE '%bhx%' --  and dv.detection_variable_name = 'physical_activity'
        AND gef.gef_type_id = 504 -- motilitiy gef
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
            uir.pilot_code LIKE '%bhx%'
        AND gef.gef_type_id = 514 -- walking gef
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
        JOIN q0 AS tab2 ON tab1.user_in_role_id = tab2.user_in_role_id
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
        JOIN q0 AS tab2 ON tab1.user_in_role_id = tab2.user_in_role_id
        AND tab1.gef_type_id = tab2.gef_type_id
        AND tab1.nui_type_id = tab2.nui_type_id
        WHERE
            tab2.interval_start = tab1.interval_start - INTERVAL '1 month'
    ), res as 
    (SELECT DISTINCT
    -- count (*) as cnt,
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
        q1.risk_status,
    nui2.nui_value as zero_value,
        --         CASE
        --         WHEN q1.user_in_role_id = 129
        --         AND q1.gef_value = 1.5 
        --           THEN
        --             'A'
        --         ELSE
        --             q1.risk_status
        --         END AS risk_status,
        q1.data_validity_status,
        q1.assessment_comment 
    FROM
        q1
    JOIN gef_dif ON (
        q1.user_in_role_id = gef_dif.user_in_role_id
        AND q1.gef_type_id = gef_dif.gef_type_id
        AND q1.time_interval_id = gef_dif.time_interval_id
    )
    JOIN nui_dif ON (
        q1.user_in_role_id = nui_dif.user_in_role_id
        AND nui_dif.gef_type_id = q1.gef_type_id
        AND q1.nui_type_id = nui_dif.nui_type_id
        AND q1.time_interval_id = nui_dif.time_interval_id
    )
    join city4age_sr.numeric_indicator_value as nui2 on (
        q1.user_in_role_id = nui2.user_in_role_id
        and q1.nui_type_id = nui2.nui_type_id
    )
    AND q1.assessment_comment NOT LIKE '%August%'
    AND q1.assessment_comment NOT LIKE '%august%'
    AND q1.assessment_comment LIKE '% %' -- assessment at least a space
    AND q1.assessment_comment NOT LIKE '%Compared to previous month the number of steps increased whereas distance dropped%' -- duplicate
    AND q1.assessment_comment NOT LIKE '%Values in July 2018 plummeted%' -- there already is A assessment in July 2018
    AND q1.assessment_comment NOT LIKE '%Compared to February 2018 both walking steps and distance rose%' -- duplicate
    AND q1.assessment_comment NOT LIKE '%Slight increase in both steps and distance compared to April 2018%' -- duplicate assessment for uId 104
    --    AND q1.assessment_comment not LIKE '%In July 2018 sharp drop in values%' -- attached to July uId 114
    AND q1.assessment_comment NOT LIKE '%Compared to previous month soft activity slightly increased with a sharp decrease in both moderate and intense activity%' -- irrelevant
    AND q1.assessment_comment NOT LIKE '%Sharp reduction in walking steps and distance for July 2018%' -- two assessments A, W in July2018 for uId 117
    AND q1.assessment_comment NOT LIKE '%Values went down in July 2018%' -- there is already A for July 2018 uid 126
    AND NOT (
        q1.assessment_comment LIKE '%Sharp drop in values compared to previous month%'
        AND q1.user_in_role_id = 117
    ) -- removed W for July2018 uid 117
    AND q1.assessment_comment NOT LIKE '%only four days%'
    AND q1.assessment_comment NOT LIKE '%Discuss with geriatrician%'
    AND q1.assessment_comment NOT LIKE '%Slight reduction in values compared to June of the same year%' -- redundant assessment also there is no June 2018
    AND q1.assessment_comment NOT LIKE '%Values are the same as March of the same year%' -- redundant, there is Walking assessment for Feb18
    AND q1.assessment_comment NOT LIKE '%Values plummeted compared to February of the same year%' -- redundant, moreover this is said for Jan18
    AND q1.assessment_comment NOT LIKE '%Compared to previous month sharp drop in both steps and distance%'
    -- and q1.assessment_comment  like '%Values for July 2018 are close to zero%' -- fixed in assessed_gef_value_set
    and q1.assessment_comment not like '%slight reduction in the number of steps%' -- this is a duplicate
    -- and q1.assessment_comment like '%Values in July 2018 declined%' -- fixed in assessed_gef_value_set
    and q1.assessment_comment not like '%Sharp drop in both the number of steps and distance compared to July 2017%' --duplicate
    and q1.assessment_comment not like '%Slight reduction in walking steps%' -- redundant
    and q1.assessment_comment not like '%Both steps and distance plunged compared to September 2017%' -- only few measure points
    -- and q1.assessment_comment not like '%Sharp drop in both the number of steps and distance compared to previous month%'
    -- group BY
    -- 	q1.user_in_role_id,
    -- 	q1.interval_start,
    -- 	q1.gef_name,
    -- 	q1.gef_value,
    -- 	gef_difference,
    -- 	q1.nui_name,
    -- 	q1.nui_value,
    -- 	nui_difference,
    -- 	q1.risk_status,
    -- 	q1.data_validity_status,
    -- 	q1.assessment_comment 
    -- -- having count (*) > 1
    where nui2.id = (SELECT nui1.id                                                                        
                                                            FROM city4age_sr.numeric_indicator_value AS nui1                                                  
                                                            INNER JOIN city4age_sr.time_interval AS ti1                                                       
                                                                ON nui1.time_interval_id = ti1. ID                                                
                                                            WHERE nui1.user_in_role_id = nui2.user_in_role_id                                     
                                                            AND nui1.nui_type_id = nui2.nui_type_id                                               
                                                            ORDER BY ti1.interval_start ASC                                                       
                                                            LIMIT 1)  
    ORDER BY
    -- cnt,
    -- nui_difference desc,
        user_in_role_id,
        interval_start
    )
    select 
        res.user_in_role_id,
        res.interval_start,
        -- 	q1.time_interval_id,
        res.gef_name,
        res.gef_value,
        res.gef_difference,
        res.nui_name,
        res.nui_value,
        -- 	q1.nui_type_id,
        res.nui_difference,
        res.risk_status,
     case
        when zero_value = 0 then 0 else 
        (nui_value - zero_value) / zero_value end as perc_change,
        --         CASE
        --         WHEN q1.user_in_role_id = 129
        --         AND q1.gef_value = 1.5 
        --           THEN
        --             'A'
        --         ELSE
        --             q1.risk_status
        --         END AS risk_status,
        res.data_validity_status,
        res.assessment_comment  
    from res
    -- order by perc_change desc

    '''
    sql_with_mea = '''
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
        WHERE
            gef.gef_type_id IN (504, 514) -- walking or motility
        AND uir.pilot_code LIKE '%bhx%'
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
        WHERE
            gef.gef_type_id IN (504, 514) -- walking or motility
        AND uir.pilot_code LIKE '%bhx%'
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
            uir.pilot_code LIKE '%bhx%' --  and dv.detection_variable_name = 'physical_activity'
        AND gef.gef_type_id = 504 -- motilitiy gef
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
            uir.pilot_code LIKE '%bhx%'
        AND gef.gef_type_id = 514 -- walking gef
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
        JOIN q0 AS tab2 ON tab1.user_in_role_id = tab2.user_in_role_id
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
        JOIN q0 AS tab2 ON tab1.user_in_role_id = tab2.user_in_role_id
        AND tab1.gef_type_id = tab2.gef_type_id
        AND tab1.nui_type_id = tab2.nui_type_id
        WHERE
            tab2.interval_start = tab1.interval_start - INTERVAL '1 month'
    ), res as 
    (SELECT DISTINCT
    -- count (*) as cnt,
        q1.user_in_role_id,
        q1.interval_start,
        q1.time_interval_id,
        q1.gef_name,
        q1.gef_value,
        gef_dif.gef_value - gef_dif.gef_value_prev AS gef_difference,
        q1.nui_name,
        q1.nui_value,
        -- 	q1.nui_type_id,
        nui_dif.nui_value - nui_dif.nui_value_prev AS nui_difference,
        q1.risk_status,
        nui2.nui_value as zero_value,
        --         CASE
        --         WHEN q1.user_in_role_id = 129
        --         AND q1.gef_value = 1.5 
        --           THEN
        --             'A'
        --         ELSE
        --             q1.risk_status
        --         END AS risk_status,
        q1.data_validity_status,
        q1.assessment_comment 
    FROM
        q1
    JOIN gef_dif ON (
        q1.user_in_role_id = gef_dif.user_in_role_id
        AND q1.gef_type_id = gef_dif.gef_type_id
        AND q1.time_interval_id = gef_dif.time_interval_id
    )
    JOIN nui_dif ON (
        q1.user_in_role_id = nui_dif.user_in_role_id
        AND nui_dif.gef_type_id = q1.gef_type_id
        AND q1.nui_type_id = nui_dif.nui_type_id
        AND q1.time_interval_id = nui_dif.time_interval_id
    )
    join city4age_sr.numeric_indicator_value as nui2 on (
        q1.user_in_role_id = nui2.user_in_role_id
        and q1.nui_type_id = nui2.nui_type_id
    )
    AND q1.assessment_comment NOT LIKE '%August%'
    AND q1.assessment_comment NOT LIKE '%august%'
    AND q1.assessment_comment LIKE '% %' -- assessment at least a space
    AND q1.assessment_comment NOT LIKE '%Compared to previous month the number of steps increased whereas distance dropped%' -- duplicate
    AND q1.assessment_comment NOT LIKE '%Values in July 2018 plummeted%' -- there already is A assessment in July 2018
    AND q1.assessment_comment NOT LIKE '%Compared to February 2018 both walking steps and distance rose%' -- duplicate
    AND q1.assessment_comment NOT LIKE '%Slight increase in both steps and distance compared to April 2018%' -- duplicate assessment for uId 104
    --    AND q1.assessment_comment not LIKE '%In July 2018 sharp drop in values%' -- attached to July uId 114
    AND q1.assessment_comment NOT LIKE '%Compared to previous month soft activity slightly increased with a sharp decrease in both moderate and intense activity%' -- irrelevant
    AND q1.assessment_comment NOT LIKE '%Sharp reduction in walking steps and distance for July 2018%' -- two assessments A, W in July2018 for uId 117
    AND q1.assessment_comment NOT LIKE '%Values went down in July 2018%' -- there is already A for July 2018 uid 126
    AND NOT (
        q1.assessment_comment LIKE '%Sharp drop in values compared to previous month%'
        AND q1.user_in_role_id = 117
    ) -- removed W for July2018 uid 117
    AND q1.assessment_comment NOT LIKE '%only four days%'
    AND q1.assessment_comment NOT LIKE '%Discuss with geriatrician%'
    AND q1.assessment_comment NOT LIKE '%Slight reduction in values compared to June of the same year%' -- redundant assessment also there is no June 2018
    AND q1.assessment_comment NOT LIKE '%Values are the same as March of the same year%' -- redundant, there is Walking assessment for Feb18
    AND q1.assessment_comment NOT LIKE '%Values plummeted compared to February of the same year%' -- redundant, moreover this is said for Jan18
    AND q1.assessment_comment NOT LIKE '%Compared to previous month sharp drop in both steps and distance%'
    -- and q1.assessment_comment  like '%Values for July 2018 are close to zero%' -- fixed in assessed_gef_value_set
    and q1.assessment_comment not like '%slight reduction in the number of steps%' -- this is a duplicate
    -- and q1.assessment_comment like '%Values in July 2018 declined%' -- fixed in assessed_gef_value_set
    and q1.assessment_comment not like '%Sharp drop in both the number of steps and distance compared to July 2017%' --duplicate
    and q1.assessment_comment not like '%Slight reduction in walking steps%' -- redundant
    and q1.assessment_comment not like '%Both steps and distance plunged compared to September 2017%' -- only few measure points
    -- and q1.assessment_comment not like '%Sharp drop in both the number of steps and distance compared to previous month%'
    -- group BY
    -- 	q1.user_in_role_id,
    -- 	q1.interval_start,
    -- 	q1.gef_name,
    -- 	q1.gef_value,
    -- 	gef_difference,
    -- 	q1.nui_name,
    -- 	q1.nui_value,
    -- 	nui_difference,
    -- 	q1.risk_status,
    -- 	q1.data_validity_status,
    -- 	q1.assessment_comment 
    -- -- having count (*) > 1
    where nui2.id = (SELECT nui1.id                                                                        
                                                            FROM city4age_sr.numeric_indicator_value AS nui1                                                  
                                                            INNER JOIN city4age_sr.time_interval AS ti1                                                       
                                                                ON nui1.time_interval_id = ti1. ID                                                
                                                            WHERE nui1.user_in_role_id = nui2.user_in_role_id                                     
                                                            AND nui1.nui_type_id = nui2.nui_type_id                                               
                                                            ORDER BY ti1.interval_start ASC                                                       
                                                            LIMIT 1)  
    ORDER BY
    -- cnt,
    -- nui_difference desc,
        user_in_role_id,
        interval_start
    )
    select 
        res.user_in_role_id,
        res.interval_start,
        res.time_interval_id,
        count(vmv.measure_value) as mea_num,
        res.gef_name,
        res.gef_value,
        res.gef_difference,
        res.nui_name,
        res.nui_value,
        -- 	q1.nui_type_id,
        res.nui_difference,
        res.risk_status,
     case
        when zero_value = 0 then 0 else 
        (nui_value - zero_value) / zero_value end as perc_change,
        res.data_validity_status,
        res.assessment_comment	
    from res
    join city4age_sr.variation_measure_value as vmv on res.user_in_role_id = vmv.user_in_role_id and vmv.measure_type_id = 91 
    join city4age_sr.time_interval as ti on vmv.time_interval_id = ti.id 
    where date_part('month', ti.interval_start) = date_part('month', res.interval_start) and 
    date_part('year', ti.interval_start) = date_part('year', res.interval_start)
    
    group by 
        res.user_in_role_id,
        res.interval_start,
        res.time_interval_id,
        res.gef_name,
        res.gef_value,
        res.gef_difference,
        res.nui_name,
        res.nui_value,
        -- 	q1.nui_type_id,
        res.nui_difference,
        res.risk_status,
        perc_change,
        res.data_validity_status,
        res.assessment_comment    
    '''
    # where risk_status in ('W', 'A')
    cur = conn.cursor()
    cur.execute(sql_with_mea)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [item[0] for item in cur.description]
    # df.to_csv('Images/output.csv')
    return df


def get_all_perc_changes():
    conn = psycopg2.connect(host = 'localhost', port = 5432, dbname = 'city4age', user = 'city4age_dba', password = 'city4age_dba')
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
        WHERE
            gef.gef_type_id IN (504, 514) -- walking or motility
        AND uir.pilot_code LIKE '%bhx%'
    ),
     interm AS (
        SELECT
            q0_gef.user_in_role_id,
            q0_gef.gef_type_id,
            q0_gef.nui_type_id,
            q0_gef.interval_start,
            q0_gef.nui_value AS cur_val,
            nui2.nui_value AS zero_val
        FROM
            q0_gef
        JOIN city4age_sr.numeric_indicator_value AS nui2 ON (
            q0_gef.user_in_role_id = nui2.user_in_role_id
            AND q0_gef.nui_type_id = nui2.nui_type_id
        )
        WHERE
            nui2. ID = (
                SELECT
                    nui1. ID
                FROM
                    city4age_sr.numeric_indicator_value AS nui1
                INNER JOIN city4age_sr.time_interval AS ti1 ON nui1.time_interval_id = ti1. ID
                WHERE
                    nui1.user_in_role_id = nui2.user_in_role_id
                AND nui1.nui_type_id = nui2.nui_type_id
                ORDER BY
                    ti1.interval_start ASC
                LIMIT 1
            )
    ) SELECT
        interm.user_in_role_id,
        interm.gef_type_id,
        dv.detection_variable_name AS nui_name,
        interm.interval_start,
        -- interm.nui_value as cur_val,
        CASE
    WHEN interm.zero_val = 0 THEN
        0
    ELSE
        (
            interm.cur_val - interm.zero_val
        ) / interm.zero_val
    END AS perc_change
    FROM
        interm
    JOIN city4age_sr.cd_detection_variable AS dv ON interm.nui_type_id = dv. ID
    '''
    cur = conn.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [item[0] for item in cur.description]
    # to_xlxs(df, 'all_perc_changes')
    return df


def prepare_and_save(data):
    # print (data)
    data.loc[:,'interval_start'] = [datum.strftime('%Y-%m-%d') for datum in data['interval_start']]
    data.loc[:,'interval_start'] = [datetime.datetime.strptime(datum, '%Y-%m-%d') for datum in data['interval_start']]
    pivoted_data = pd.pivot_table(data, index = ['user_in_role_id', 'interval_start'], columns='nui_name', values=['perc_change'], aggfunc=np.max)
    pivoted_data.columns = [f'{j}_{i}' for i, j in pivoted_data.columns]
    pivoted_data = pivoted_data.reset_index()
    # print (pivoted_data.iloc[:, 3:]!=0)
    pivoted_data = pivoted_data.loc[(pivoted_data.iloc[:, 3:]!=0).any(axis=1)]
    to_xlxs(pivoted_data, 'all_perc_changes')

def prepare_data(data):
    data = data[data['data_validity_status']=='V']
    risk_mapping = {'A': 2, 'W':1, 'N': 0}
    nui_name_mapping = {label : idx for idx, label in enumerate(np.unique(data['nui_name']))}
    # data['nui_name'] = data['nui_name'].map(nui_name_mapping)
    data.loc[:,'risk_status'] = data['risk_status'].map(risk_mapping)
    data.loc[:,'interval_start'] = [datum.strftime('%Y-%m-%d') for datum in data['interval_start']]
    data.loc[:,'interval_start'] = [datetime.datetime.strptime(datum, '%Y-%m-%d') for datum in data['interval_start']]
    data = data[['user_in_role_id', 'interval_start', 'gef_name', 'gef_value', 'gef_difference', 'nui_name', 'mea_num', 'nui_value', 'nui_difference', 'perc_change', 'risk_status', 'data_validity_status', 'assessment_comment']]
    return data


def to_xlxs(data, name):
    writer = pd.ExcelWriter("Data//" + name +'.xlsx', engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1')
    data.to_csv("Data//" + name +'.csv')
    writer.save()


def get_motility_data(data):
    motility_data = data[(data['gef_name']=='motility') | (data['gef_name']=='walking')]
    # to_xlxs(motility_data, name='raw_assessments_1710_multi')
    motility_data = pd.pivot_table(motility_data, index =['interval_start', 'user_in_role_id', 'assessment_comment', 'mea_num', 'risk_status', 'gef_value', 'gef_difference'],
                                   columns = 'nui_name', values= ['nui_value', 'nui_difference', 'perc_change'], aggfunc= np.max)
    motility_data.columns = [f'{j}_{i}' for i, j in motility_data.columns]
    motility_data = motility_data.reset_index()
    motility_data=motility_data.sort_values('risk_status')
    motility_data.reset_index(drop= True, inplace=True)
    to_xlxs(motility_data, name = 'assessments_2310_multi_5')
    return motility_data.iloc[:,3:]

def lam1(x):
    return np.percentile(x, 25)

def lam2(x):
    return np.percentile(x, 50)

def find_perc_chg():
    motility_data = pd.read_csv("Data//raw_assessments_1710_multi.csv")
    # motility_data.plot('')
    # gr_data = motility_data.groupby(['nui_name', 'risk_status'])['perc_change'].min()
    pivoted_data = pd.pivot_table(motility_data, index = ['nui_name', 'risk_status'], values='perc_change', aggfunc=[np.min, np.max, lam1, lam2, np.mean, np.std]).reset_index()
    # to_xlxs(pivoted_data, "perc_chg")
    print(pivoted_data)


