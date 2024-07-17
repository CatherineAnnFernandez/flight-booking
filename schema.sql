CREATE DATABASE tickets;

USE tickets;

CREATE TABLE available_flights (
    flight_id INT PRIMARY KEY,
    departure_city VARCHAR(50),
    destination_city VARCHAR(50),
    departure_month VARCHAR(20),
    departure_date DATE
);

CREATE TABLE flight_details (
    flight_id INT PRIMARY KEY,
    departure_time TIME,
    arrival_time TIME,
    airline VARCHAR(50),
    seats INT,
    FOREIGN KEY (flight_id) REFERENCES available_flights(flight_id)
);
