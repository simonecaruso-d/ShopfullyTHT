-- DimWeatherCondition
CREATE TABLE "DimWeatherCondition" ("Id" INT PRIMARY KEY,
                                    "MainCondition" VARCHAR(100) NOT NULL,
                                    "DetailedCondition" VARCHAR(250) NOT NULL,
                                    "CreatedAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                                    "UpdatedAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                                    
                                    CONSTRAINT "UQWC" UNIQUE("MainCondition", "DetailedCondition"));

-- DimCity
CREATE TABLE "DimCity" ("Id" INT PRIMARY KEY,
                        "Name" VARCHAR(100) NOT NULL,
                        "Latitude" NUMERIC(8,6) NOT NULL,
                        "Longitude" NUMERIC(9,6) NOT NULL,
                        "Province" VARCHAR(100) NOT NULL,
                        "Region" VARCHAR(100) NOT NULL,
                        "Country" VARCHAR(100) NOT NULL,
                        "CreatedAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                        "UpdatedAt" TIMESTAMP NOT NULL DEFAULT NOW(),
    
                        CONSTRAINT "UQ_DimCity_Name" UNIQUE ("Name"));

CREATE INDEX "IdxCity" ON "DimCity"("Name");

-- FactWeather
CREATE TABLE "FactWeather" ("Id" BIGSERIAL PRIMARY KEY,
                            "CTId" INT NOT NULL,
                            "WCId" INT NOT NULL,
                            "FullTimestamp" TIMESTAMP NOT NULL,
                            "DataType" VARCHAR(20) NOT NULL CHECK ("DataType" IN ('Actual', 'Forecast')), 
                            "Temperature" NUMERIC(5,2),
                            "FeltTemperature" NUMERIC(5,2),
                            "Humidity" NUMERIC(5,2),
                            "Clouds" NUMERIC(5,2),
                            "WindSpeed" NUMERIC(5,2),
                            "RainProbability" NUMERIC(5,2),
                            "RainVolume" NUMERIC(6,2),
                            "RetrievalTime" TIMESTAMP NOT NULL DEFAULT NOW(),
                            "IsCurrent" BOOLEAN DEFAULT TRUE,

                            CONSTRAINT "FactCity" FOREIGN KEY("CTId") REFERENCES "DimCity"("Id"),
                            CONSTRAINT "FactWeatherCondition" FOREIGN KEY("WCId") REFERENCES "DimWeatherCondition"("Id"));

CREATE UNIQUE INDEX "FactCurrent" ON "FactWeather"("CTId", "FullTimestamp", "DataType") WHERE "IsCurrent" = TRUE;
CREATE INDEX "IdxFWCityDate" ON "FactWeather"("CTId", "FullTimestamp");
CREATE INDEX "IdxFWDate" ON "FactWeather"("FullTimestamp");
CREATE INDEX "IdxFWDataType" ON "FactWeather"("DataType");
CREATE INDEX "IdxIsCurrent" ON "FactWeather"("IsCurrent");