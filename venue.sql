CREATE TABLE Venue (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Latitude DECIMAL(10, 6),
    Longitude DECIMAL(10, 6)
);

-- Inserting venue id's data into the Venue table
INSERT INTO Venue (Id, Name, Latitude, Longitude)
VALUES 
    (1, 'Venue1', 52.52, 13.41),
    (2, 'Venue2', -30.00, 153.125),
    (3, 'Venue3', 44.4375, 26.125);