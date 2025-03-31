CREATE TABLE Weather (
    id INT PRIMARY KEY AUTO_INCREMENT,
    venue_id INT,
    timestamp DATETIME,
    temperature FLOAT,
    humidity FLOAT,
    dewpoint FLOAT,
    apparent_temp FLOAT,
    precipitation FLOAT,
    precipitation_prob FLOAT,
    rain FLOAT,
    showers FLOAT,
    snowfall FLOAT,
    snow_depth FLOAT,
    FOREIGN KEY (venue_id) REFERENCES Venue(id)
);