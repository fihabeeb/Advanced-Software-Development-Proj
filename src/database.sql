-- # SIGNATURES FROM STUDENTS: Fadil Idris Habeeb(22066955), Silas Desmond(22029026)
DROP SCHEMA IF EXISTS horizon_cinemas;
CREATE DATABASE horizon_cinemas;

USE horizon_cinemas;

CREATE TABLE Cinema
(
    CinemaId int not null auto_increment,
    primary key (CinemaId),
    Name VARCHAR(40),
    CinemaLocation VARCHAR(40)
);



CREATE TABLE Employees
(
	EmployeeID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (EmployeeID),
    UserPassword VARCHAR(90) NULL,
    Name VARCHAR(40) NULL,
	PrivilageLevel INT NULL DEFAULT 1
);
-- we need an actors table i think


insert into Employees ( EmployeeID, UserPassword, Name, PrivilageLevel)
VALUES (1, '$5$rounds=535000$gSVcf7c811eFeGlQ$3swB1f6Al.yte1xNVYJo41enkYuMFtHMLY/cDd5zSUD', "Jason", 1),
(2,'$5$rounds=535000$t.58mD9PSPWmO6H0$DDSonZhOYSPnf7HT9V/qXJiNvXQlKWkSnQpXIvUkm9.', "Kevin", 2),
(3, '$5$rounds=535000$lQePl0UL96bLy8dh$vioNDEL0g1IibMj7G/PxChMZHLpnfsGwgzrapaFAJo6', "Tyler", 3);
-- SELECT * FROM Employees;


CREATE TABLE Screen
(
    ScreenId int not null auto_increment,
    primary key (ScreenId),
    maxCapacity int null,
    CinemaId int null,
    FOREIGN KEY (CinemaId)
		REFERENCES Cinema (CinemaId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


CREATE TABLE Film
(
	FilmId INT NOT NULL auto_increment,
    PRIMARY KEY (FilmId),
    Title VARCHAR(60) NULL,
    Genre Varchar(20) NULL,
    Duration TIME null,
    Rating VARCHAR(20) null,
    CinemaId int null,
    FOREIGN KEY (CinemaId)
		REFERENCES Cinema (CinemaId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Shows
(
    ShowsId int not null auto_increment,
    primary key (ShowsId),
    ShowTime Time null,
    priceLowerHall double NULL,
    priceUpperHall double null,
    FilmId int null,
    ScreenId int null,
    CinemaId int null,
    LowerHallCapacity int null,
    UpperHallCapacity int null,
    VIPHallCapacity int null,
    FOREIGN KEY (CinemaId)
		REFERENCES Cinema (CinemaId)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (FilmId)
		REFERENCES Film (FilmId)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	FOREIGN KEY (ScreenId)
		REFERENCES Screen (ScreenId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);



CREATE TABLE Actors
(
	ActorId INT NOT NULL auto_increment,
    primary key (ActorId),
    ActorName VARCHAR(40),
    FilmId int null,
    FOREIGN KEY (FilmID)
		REFERENCES Film (FilmID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


-- Start here


CREATE TABLE Booking
(
    BookingId int not null auto_increment,
    primary key (BookingId),
    BookingReference VARCHAR(40),
    CustomerName VARCHAR(40),
    BookingDate datetime null,
    TotalCost double null,
    BookingStatus VARCHAR(30),
    ShowsId int null,
    EmployeeID int null,

    FOREIGN KEY (ShowsId)
		REFERENCES Shows (ShowsId)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (EmployeeID)
		REFERENCES Employees (EmployeeID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
    -- ticket and booking table

);

CREATE TABLE Billings
(
    BillingsId int not null AUTO_INCREMENT,
    PRIMARY key (BillingsId),
    PaymentAmount double null,
    -- payement type 1 means income, payement type 2 means refund
    PaymentType int null,
    BookingId int null,
    FOREIGN KEY (BookingId)
		REFERENCES Booking (BookingId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


CREATE TABLE Seats
(
    SeatsId int not null auto_increment,
    primary key (SeatsId),
    SeatNumber VARCHAR(40),
    SeatType int,
    IsAvailable BOOLEAN,
    ScreenId int null,
    FOREIGN KEY (ScreenId)
		REFERENCES Screen (ScreenId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


CREATE TABLE Tickets
(
    TicketId int not null auto_increment,
    primary key (TicketId),
    Price Float null,
    TicketType VARCHAR(40),
    SeatsId INT NULL,
    BookingId int null,
    FOREIGN KEY (SeatsId)
		REFERENCES Seats (SeatsId)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	FOREIGN KEY (BookingId)
		REFERENCES Booking (BookingId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


insert into Cinema ( CinemaId, Name, CinemaLocation)
VALUES (1, "Bris1", "Bristol"),
(2,"Birm1", "Birmingham"),
(3, "Bris2", "Bristol"),
(4,"Birm2", "Birmingham"),
(5, "Card1", "Cardiff"),
(6,"Lond1", "London"),
(7, "Card2", "Cardiff"),
(8,"Lond2", "London");

-- Mock data for Screen table
INSERT INTO Screen (maxCapacity, CinemaId) VALUES
(120, 3),
(120, 4),
(120, 5),
(120, 6),
(120, 7),
(120, 7),
(60, 8),
(60, 8),
(60, 1),
(60, 1),
(60, 1),
(60, 2),
(60, 2),
(60, 2),
(60, 3),
(60, 3),
(60, 3),
(60, 4),
(60, 4),
(60, 5),
(60, 4),
(60, 4),
(90, 4),
(90, 4),
(90, 5),
(90, 5),
(90, 5),
(90, 5),
(90, 5),
(90, 5),
(90, 6),
(90, 6),
(90, 6),
(90, 6),
(90, 6),
(90, 6),
(90, 7),
(90, 7),
(90, 7),
(90, 7),
(90, 7),
(90, 7),
(90, 8),
(90, 8),
(90, 8),
(90, 8),
(90, 8),
(90, 8);

-- Mock data for Film table
INSERT INTO Film (Title, Genre, Duration, Rating, CinemaId) VALUES
('Avatar', 'Sci-Fi', '2:45', 'PG-13', 3),
('Gladiator', 'Drama', '2:35', 'R', 4),
('Frozen', 'Animation', '1:50', 'PG', 5),
('Avengers: Endgame', 'Action', '3:00', 'PG-13', 6),
('Titanic', 'Romance', '3:15', 'PG-13', 7),
('The Lion King', 'Animation', '1:40', 'PG', 8),
('Joker', 'Thriller', '2:05', 'R', 1),
('Parasite', 'Thriller', '2:12', 'R', 2),
('Toy Story', 'Animation', '1:30', 'G', 3),
('The Godfather', 'Crime', '2:55', 'R', 4),
('Pulp Fiction', 'Crime', '2:58', 'R', 5),
('Finding Nemo', 'Animation', '1:40', 'PG', 6),
('The Matrix', 'Sci-Fi', '2:16', 'R', 7),
('Spider-Man: No Way Home', 'Action', '2:28', 'PG-13', 8),
('The Shawshank Redemption', 'Drama', '2:22', 'R', 1),
('Forrest Gump', 'Drama', '2:22', 'PG-13', 2),
('The Incredibles', 'Animation', '1:55', 'PG', 3),
('Coco', 'Animation', '1:45', 'PG', 4),
('Black Panther', 'Action', '2:14', 'PG-13', 5),
('A Quiet Place', 'Horror', '1:30', 'PG-13', 6);

-- Mock data for Shows table
-- Price upper should always be 120% of the value of price lower
INSERT INTO Shows (ShowTime, priceLowerHall, priceUpperHall, FilmId, ScreenId, CinemaId, LowerHallCapacity, UpperHallCapacity, VIPHallCapacity) VALUES
-- Films with 1 showtime
('10:00:00', 6.0, 7.2, 1, 1, 3, 40, 70, 10), -- Morning, Cinema 3
('13:00:00', 6.0, 7.2, 2, 2, 4, 40, 70, 10), -- Afternoon, Cinema 4
('17:45:00', 7.0, 8.4, 3, 3, 5, 40, 70, 10), -- Evening, Cinema 5
('20:30:00', 12.0, 14.4, 4, 4, 6, 40, 70, 10), -- Evening, Cinema 6

-- Films with 2 showtimes
('08:30:00', 5.0, 6.0, 5, 5, 7, 40, 70, 10), -- Morning, Cinema 7
('18:00:00', 7.0, 8.4, 5, 6, 7, 40, 70, 10), -- Evening, Cinema 7
('10:15:00', 10.0, 12.0, 6, 7, 8, 40, 70, 10), -- Morning, Cinema 8
('19:45:00', 12.0, 14.4, 6, 8, 8, 40, 70, 10), -- Evening, Cinema 8

-- Films with 3 showtimes
('09:00:00', 6.0, 7.2, 7, 9, 1, 20, 30, 10), -- Morning, Cinema 1
('14:15:00', 7.0, 8.4, 7, 10, 1, 20, 30, 10), -- Afternoon, Cinema 1
('20:15:00', 5.0, 9.6, 7, 11, 1, 20, 30, 10), -- Evening, Cinema 1
('11:45:00', 5.0, 6.0, 8, 12, 2, 20, 30, 10), -- Morning, Cinema 2
('16:30:00', 6.0, 7.2, 8, 13, 2, 20, 30, 10), -- Afternoon, Cinema 2
('19:30:00', 7.0, 8.4, 8, 14, 2, 20, 30, 10), -- Evening, Cinema 2

-- Remaining films with additional showtimes to fill gaps
('09:45:00', 6.0, 7.2, 9, 15, 3, 40, 70, 10), -- Morning, Cinema 3
('15:30:00', 7.0, 8.4, 9, 16, 3, 40, 70, 10), -- Afternoon, Cinema 3
('20:00:00', 8.0, 9.6, 9, 17, 3, 40, 70, 10), -- Evening, Cinema 3
('10:30:00', 5.0, 6.0, 10, 18, 4, 40, 70, 10), -- Morning, Cinema 4
('17:00:00', 7.0, 8.4, 10, 19, 4, 40, 70, 10), -- Evening, Cinema 4
('12:00:00', 6.0, 7.2, 11, 20, 5, 40, 70, 10); -- Afternoon, Cinema 5

-- Each film needs actors
INSERT INTO Actors (ActorName, FilmId) VALUES
('Leonardo DiCaprio', 1),
('Christian Bale', 2),
('Matthew McConaughey', 3),
('Sam Worthington', 4),
('Russell Crowe', 5),
('Idina Menzel', 6),
('Robert Downey Jr.', 7),
('Kate Winslet', 8),
('Donald Glover', 9),
('Joaquin Phoenix', 10),
('Song Kang-ho', 11),
('Tom Hanks', 12),
('Al Pacino', 13),
('Uma Thurman', 14),
('Ellen DeGeneres', 15),
('Keanu Reeves', 16),
('Tom Holland', 17),
('Morgan Freeman', 18),
('Robin Wright', 19),
('Holly Hunter', 20);

-- Mock data for Booking table
-- INSERT INTO Booking (BookingReference, CustomerName, BookingDate, TotalCost, BookingStatus, ShowsId) VALUES
-- ('BR1234', 'John Doe', '2025-03-10 12:30:00', 30.0, "Active",1),
-- ('BR1235', 'Jane Smith', '2025-05-11 16:45:00', 36.0, "Active",2),
-- ('BR1236', 'Alice Brown', '2025-06-12 19:15:00', 34.0, "Active",3);

-- Mock data for Seats table
INSERT INTO Seats (SeatNumber, SeatType, IsAvailable, ScreenId) VALUES
('A1', 1, TRUE, 1),
('B2', 2, TRUE, 2),
('C3', 1, FALSE, 3),
('A1', 1, TRUE, 4),
('B2', 2, TRUE, 5),
('C3', 1, FALSE, 6),
('A1', 1, TRUE, 7),
('B2', 2, TRUE, 8),
('C3', 1, FALSE, 9),
('A1', 1, TRUE, 10),
('B2', 2, TRUE, 11),
('C3', 1, FALSE, 12),
('A1', 1, TRUE, 13),
('B2', 2, TRUE, 14),
('C3', 1, FALSE, 15),
('A1', 1, TRUE, 16),
('B2', 2, TRUE, 17),
('C3', 1, FALSE, 18),
('A1', 1, TRUE, 19),
('B2', 2, TRUE, 20),
('C3', 1, FALSE, 21),
('A1', 1, TRUE, 22),
('B2', 2, TRUE, 23),
('C3', 1, FALSE, 24),
('A1', 1, TRUE, 25),
('B2', 2, TRUE, 26),
('C3', 1, FALSE, 27),
('A1', 1, TRUE, 28),
('B2', 2, TRUE, 29),
('C3', 1, FALSE, 30),
('A1', 1, TRUE, 31),
('B2', 2, TRUE, 32),
('C3', 1, FALSE, 33),
('A1', 1, TRUE, 34),
('B2', 2, TRUE, 35),
('C3', 1, FALSE, 36),
('A1', 1, TRUE, 37),
('B2', 2, TRUE, 38),
('C3', 1, FALSE, 39),
('A1', 1, TRUE, 40),
('B2', 2, TRUE, 41),
('C3', 1, FALSE, 42),
('A1', 1, TRUE, 43),
('B2', 2, TRUE, 44),
('C3', 1, FALSE, 45),
('A1', 1, TRUE, 46),
('B2', 2, TRUE, 47),
('C3', 1, FALSE, 48);

-- Mock data for Tickets table
-- INSERT INTO Tickets (Price, TicketType, SeatsId, BookingId) VALUES
-- (15.0, 'Adult', 1, 1),
-- (18.0, 'Adult', 2, 2),
-- (17.0, 'Adult', 3, 3);

-- SHOW TABLES;