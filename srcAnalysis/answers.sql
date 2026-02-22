-- Question | How many distinct weather conditions were observed (rain/snow/clear/…) in a certain period?
                SELECT COUNT (DISTINCT "WCId")
                FROM "FactWeather"
                WHERE "DataType" = 'Actual' AND "FullTimestamp" <= '2026-02-19 04:00:00' AND "IsCurrent" = TRUE;
-- Comments | I decided the time limit to have at least a difference of 1 in the count compared to the query without the time limit. 
--            I also decided to use the "Actual" data type since the question is about observed ("were") weather conditions.           
-- Answer   | Supabase returns correctly a value equal to 9.

-- Question | Can you rank the most common weather conditions in a certain period of time per city?
                SELECT c."Name", wc."MainCondition", COUNT (fw."FullTimestamp") AS "Count"
                FROM "FactWeather" fw
                LEFT JOIN "DimCity" c ON fw."CTId" = c."Id"
                LEFT JOIN "DimWeatherCondition" wc ON fw."WCId" = wc."Id"
                WHERE fw."DataType" = 'Forecast' AND fw."FullTimestamp" >= '2026-02-24 11:00:00' AND fw."IsCurrent" = TRUE
                GROUP BY c."Name", wc."MainCondition"
                ORDER BY c."Name", "Count" DESC;
-- Comments | Here I decided to use the "Forecast" data type for the sake of variety. I also took a date that limits the number of results for the sake of visibility.
-- Answer   | Supabase returns correctly the following table:
                [{"Name": "Bologna", "MainCondition": "Clouds","Count": 4},
                {"Name": "Bologna", "MainCondition": "Clear", "Count": 1},
                {"Name": "Cagliari", "MainCondition": "Clear", "Count": 5},
                {"Name": "Milano", "MainCondition": "Clear", "Count": 3},
                {"Name": "Milano", "MainCondition": "Clouds", "Count": 2}]

-- Question | What are the temperature averages observed in a certain period per city? 
                SELECT c."Name", ROUND(AVG(fw."Temperature"), 2) AS "AverageTemperature"
                FROM "FactWeather" fw
                LEFT JOIN "DimCity" c ON fw."CTId" = c."Id"
                WHERE fw."DataType" = 'Actual' AND fw."FullTimestamp" <= '2026-02-19 04:00:00' AND fw."IsCurrent" = TRUE
                GROUP BY c."Name" 
                ORDER BY "AverageTemperature" ASC;
-- Answer   | Supabase returns correctly the following table:
                [{"Name": "Milano", "AverageTemperature": "8.32"},
                {"Name": "Bologna", "AverageTemperature": "9.30"},
                {"Name": "Cagliari", "AverageTemperature": "13.03"}]

-- Question | What city had the highest absolute temperature in a certain period of time?
                WITH MaxTemperatureTable AS (SELECT MAX("Temperature") AS maxTemperature FROM "FactWeather" WHERE "DataType" = 'Actual' AND "FullTimestamp" <= '2026-02-19 04:00:00')

                SELECT c."Name"
                FROM "FactWeather" fw
                JOIN MaxTemperatureTable mtt ON fw."Temperature" = mtt.maxTemperature
                LEFT JOIN "DimCity" c ON fw."CTId" = c."Id"
                WHERE fw."DataType" = 'Actual' AND fw."FullTimestamp" <= '2026-02-19 04:00:00' AND fw."IsCurrent" = TRUE;
-- Answer   | Supabase returns correctly a value equal to Cagliari.

-- Question | Which city had the highest daily temperature variation in a certain period of time? 
                SELECT "Date", "Name"
                FROM 
                    (SELECT CAST(fw."FullTimestamp" AS DATE) AS "Date", c."Name", 
                            RANK() OVER (PARTITION BY CAST(fw."FullTimestamp" AS DATE) ORDER BY (MAX(fw."Temperature") - MIN(fw."Temperature")) DESC) as Ranking
                    FROM "FactWeather" fw
                    LEFT JOIN "DimCity" c ON fw."CTId" = c."Id"
                    WHERE fw."DataType" = 'Actual' AND fw."FullTimestamp" <= '2026-02-19 04:00:00' AND fw."IsCurrent" = TRUE
                    GROUP BY "Date", c."Name")
                WHERE Ranking = 1;
-- Answer   | Supabase returns correctly the following table:
                [{"Date": "2026-02-18", "Name": "Cagliari"},
                {"Date": "2026-02-19", "Name": "Milano"}]

-- Question | What city had the strongest wind in a certain period of time?
                WITH MaxWindTable AS (SELECT MAX("WindSpeed") AS maxWind FROM "FactWeather" WHERE "DataType" = 'Actual' AND "FullTimestamp" <= '2026-02-19 04:00:00')

                SELECT c."Name"
                FROM "FactWeather" fw
                JOIN MaxWindTable mwt ON fw."WindSpeed" = mwt.maxWind
                LEFT JOIN "DimCity" c ON fw."CTId" = c."Id"
                WHERE fw."DataType" = 'Actual' AND fw."FullTimestamp" <= '2026-02-19 04:00:00' AND fw."IsCurrent" = TRUE;
-- Answer   | Supabase returns correctly the following table:
                [{"Name": "Milano"},
                {"Name": "Cagliari"}]