# SIGNATURES FROM STUDENTS: Fadil Idris Habeeb(22066955)
from datetime import datetime as dateTime
import mysql.connector, dbconnect
from passlib.hash import sha256_crypt

DB_NAME = 'Horizon Cinemas'

class Seat:
    def __init__(self, _seatNumber: str, _type: int, _available: bool):
        self.__seatNumber: str = _seatNumber
        self.__type: int = _type
        self.__available: bool = _available
        if self.__seatNumber == None:
            database = dbconnect.getConnection()
            if database.is_connected():
                cursor_obj = database.cursor()
                query = "SELECT SeatsId FROM Seats ORDER BY SeatsId DESC LIMIT 1"
                cursor_obj.execute(query,)
                self.__seatNumber = int(cursor_obj.fetchone()[0])
            database.commit()

    def getSeatNumber(self) -> str:
        return self.__seatNumber

    def setSeatNumber(self, input: str) -> None:
        self.__seatNumber = input

    def getType(self) -> int:
        return self.__type

    def setType(self, input) -> None:
        self.__available = input

    def getAvailable(self) -> bool:
        return self.__available

    def setAvailable(self, input: bool) -> None:
        self.__available = input

    def commitToDB(self) -> bool:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            pushSql = "INSERT INTO Seats (SeatNumber, SeatType, IsAvailable) VALUES (%s, %s, %s)"

            input = (self.__seatNumber, self.__type, self.__available)
            cursor_obj.execute(pushSql, input)
            database.commit()

class Ticket:
    def __init__(self, inputId: str, inputTicketType: str, inputSeat: Seat, inputPrice: float):
        self.__id: str = inputId
        self.__ticketType: str = inputTicketType
        self.__seat: Seat = inputSeat
        self.__price: float = inputPrice
        if self.__id == None:
            database = dbconnect.getConnection()
            if database.is_connected():
                cursor_obj = database.cursor()
                query = "SELECT TicketId FROM Tickets ORDER BY TicketId DESC LIMIT 1"
                cursor_obj.execute(query,)
                if cursor_obj.fetchone():
                    self.__id = int(cursor_obj.fetchone()[0])
                else:
                    self.__id = 1
                database.commit()

    def getId(self) -> str:
        return self.__id

    def setId(self, input: str) -> None:
        self.__id = input

    def getTicketType(self) -> str:
        return self.__ticketType

    def setTicketType(self, input: str) -> None:
        self.__ticketType = input

    def getSeat(self) -> Seat:
        return self.__seat

    def getPrice(self) -> float:
        return self.__price

    def setPrice(self, input: float) -> None:
        self.__price = input


    def commitToDB(self) -> bool:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            pushSql = "INSERT INTO Tickets (TicketId, Price, TicketType, SeatsId) VALUES (%s, %s, %s, %s)"

            input = (self.__id, self.__price, self.__ticketType, self.__seat.getSeatNumber())
            cursor_obj.execute(pushSql, input)
            database.commit()

class Film():
    def __init__(self, _title: str, _genre: str, _duration: dateTime, _rating: str, _actors: list[str], _filmId: int = None) -> None:
        self.__filmId: int = _filmId
        self.__title: str =  _title
        self.__genre: str = _genre
        self.__duration: dateTime = _duration
        self.__rating: str = _rating
        self.__actors: list[str] = _actors


    def addActor(self,_actor: str) -> None:
        self.__actors.append(_actor)

    def getTitle(self) -> str:
        return self.__title

    def setTitle(self, input: str) -> None:
        self.__title = input

    def getGenre(self) -> str:
        return self.__genre

    def setGenre(self, input: str) -> None:
        self.__genre = input

    def getDuration(self) -> dateTime:
        return self.__duration

    def setDuration(self, input: dateTime) -> None:
        self.__duration = input

    def getRating(self) -> str:
        return self.__rating

    def setRating(self, input: str):
        self.__rating = input

    def getActors(self) -> list[str]:
        return self.__actors

    def setActors(self, input: list[str]) -> None:
        self.__actors = input

    def getFilmId(self) -> int:
        return self.__filmId

    def setFilmId(self, input: int) -> None:
        self.__filmId = input

    def commitToDB(self) -> bool:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            pushSql = "INSERT INTO Film (FilmId, Title, Genre, Duration, Rating) VALUES (%s, %s, %s, %s, %s)"

            input = (self.__filmId, self.__title, self.__genre, self.__duration, self.__rating)
            cursor_obj.execute(pushSql, input)
            database.commit()

class Screen:
    def __init__(self, inputScreenNum: int, inputCapacity, inputSeats: list[Seat]) -> None:
        self.__screenNumber: int = inputScreenNum
        self.__capacity: int = inputCapacity
        self.__seats: list[Seat] = inputSeats

    def getScreenNumber(self) -> int:
        return self.__screenNumber

    def getCapacity(self) -> int:
        return self.__capacity

    def setCapacity(self, inputCapacity: int) -> None:
        self.__capacity = inputCapacity

    def getSeats(self) -> list[Seat]:
        return self.__seats

    def setScreenNumber(self, inputNum: int) -> None:
        self.__screenNumber = inputNum


    def setSeats(self, inputSeats: list[Seat]) -> None:
        self.__seats = inputSeats


class Show:
    def __init__(self, inputShowTime: dateTime, inputFilm: Film, inputScreen: Screen, inputPriceLower: float, inputPriceUpper: float, _showId: int, inputLowerCapacity: int, inputUpperCapacity: int, inputVIPCapacity: int) -> None:
        self.__showId: int = _showId
        self.__showTime:dateTime = inputShowTime
        self.__film: Film = inputFilm
        self.__screen: Screen = inputScreen
        self.__priceLower: float = inputPriceLower
        self.__priceUpper: float = inputPriceUpper
        self.__capacityLowerHall: int = inputLowerCapacity
        self.__capacityUpperHall: int = inputUpperCapacity
        self.__capacityVIPHall: int = inputVIPCapacity

    def getShowTime(self) -> dateTime:
        return self.__showTime

    def setShowTime(self, inputShowTime: dateTime) -> None:
        self.__showTime = inputShowTime

    def getCapacityLower(self) -> int:
        return self.__capacityLowerHall

    def setCapacityLower(self, inputCapacity: int) -> None:
        self.__capacityLowerHall = inputCapacity

    def getCapacityUpper(self) -> int:
        return self.__capacityUpperHall

    def setCapacityUpper(self, inputCapacity: int) -> None:
        self.__capacityUpperHall = inputCapacity

    def getCapacityVIP(self) -> int:
        return self.__capacityVIPHall

    def setCapacityVIP(self, inputCapacity: int) -> None:
        self.__capacityVIPHall = inputCapacity

    def getFilm(self) -> Film:
        return self.__film

    def setFilm(self, inputFilm: Film) -> Film:
        self.__film = inputFilm

    def getScreen(self) -> Screen:
        return self.__screen

    def setScreen(self, inputScreen: Screen) -> None:
        self.__screen = inputScreen

    def getPriceLower(self) -> float:
        return self.__priceLower

    def setPriceLower(self, setPrice: float) -> None:
        self.__priceLower = setPrice

    def getPriceUpper(self) -> float:
        return self.__priceUpper

    def setPriceUpper(self, setPrice: float) -> None:
        self.__priceUpper = setPrice

    def setShowId(self, input: int) -> None:
        self.__showId = input

    def getShowId(self) -> int:
        return self.__showId

    def UpdateInDB(self):
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            changeSql = "UPDATE Shows set LowerHallCapacity = (%s), UpperHallCapacity = (%s), VIPHallCapacity = (%s) WHERE ShowsId = (%s)"
            cursor_obj.execute(changeSql, (self.getCapacityLower(), self.getCapacityUpper(), self.getCapacityVIP(), self.getShowId()))
            database.commit()
            return True

    def commitToDB(self, _potentialCinemaPlace: int = None) -> bool:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            if _potentialCinemaPlace == 0:
                pushSql = "INSERT INTO Shows (ShowsId, ShowTime, priceLowerHall, priceUpperHall, FilmId, ScreenId, LowerHallCapacity, UpperHallCapacity, VIPHallCapacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                input = (self.__showId, self.__showTime, self.__priceLower, self.__priceUpper, self.__film.getFilmId(), self.__screen.getScreenNumber(), int(float(self.__screen.getCapacity() * 1/3)), int(float(self.__screen.getCapacity() * 2/3) - 10), 10)
                cursor_obj.execute(pushSql, input)
            else:
                pushSql = "INSERT INTO Shows (ShowsId, ShowTime, priceLowerHall, priceUpperHall, FilmId, CinemaId, ScreenId, LowerHallCapacity, UpperHallCapacity, VIPHallCapacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                input = (self.__showId, self.__showTime, self.__priceLower, self.__priceUpper, self.__film.getFilmId(), _potentialCinemaPlace, self.__screen.getScreenNumber(), int(float(self.__screen.getCapacity() * 1/3)), int(float(self.__screen.getCapacity() * 2/3) - 10), 10)
                cursor_obj.execute(pushSql, input)
            database.commit()
        theSystem.reset()


class Cinema:
    def __init__(self, id: int, nameInput: str, locationInput: str, screensInput: list[Screen], showsInput: list[Show]) -> None:
        self.__id: int = id
        self.__name:str = nameInput
        self.__location: str = locationInput
        self.__screen: list[Screen] = screensInput
        self.__show: list[Show] = showsInput

    def getId(self) -> int:
        return self.__id

    def getName(self) -> str:
        return self.__name

    def getLocation(self) -> str:
        return self.__location

    def getScreen(self) -> list[Screen]:
        return self.__screen

    def getShow(self) -> list[Show]:
        return self.__show

    def setName(self, inputName: str) -> None:
        self.__name = inputName

    def setLocation(self, inputLocation: str) -> None:
        self.__location = inputLocation

    def setScreen(self, inputScreen: list[Screen]) -> None:
        self.__screen = inputScreen

    def setShow(self, inputShow: list[Show]) -> None:
        self.__show = inputShow

class BookingStaff():
    def __init__(self, id: int, name: str, privilageLevel: int = 1):
        self.__userId: int = id
        self.__name: str = name
        self.__privilegesLevel: int = privilageLevel
        self.__loggedIn: bool = True
        print(self.__loggedIn)

    def isLoggedIn(self) -> bool:
        return self.__loggedIn

    def createBooking(self, _bookingReference: str, _show: Show, _tickets: list[Ticket], _bookingDate: dateTime, _totalCost: float, _customerName: str) -> None:
        bookingRef = str(_show.getFilm().getTitle())[0:3] + (_customerName)[0:3] + str(int(_totalCost))[0:2] + str(_bookingDate)[0:2]
        Booking(bookingRef, _show, _tickets, _bookingDate, _totalCost, _customerName, _isGenerate=False)
        for ticket in _tickets:
            if ticket.getTicketType() == "Lower Hall":
                _show.setCapacityLower(_show.getCapacityLower() - 1)
            if ticket.getTicketType() == "Upper Hall":
                _show.setCapacityUpper(_show.getCapacityUpper() - 1)
            if ticket.getTicketType() == "Premium":
                _show.setCapacityVIP(_show.getCapacityVIP() - 1)
        _show.UpdateInDB()
        theSystem.reset()
        #_tickets[0].getTicketType()
        #_show.getScreen().setCapacityLower()

    def resetPassword(self, oldPassword: str, newPassword: str) -> bool:
        if self.__currentUser != None:
            return False
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            primarysql = "SELECT EmployeeID FROM Employees"
            cursor_obj.execute(primarysql)
            print(cursor_obj)
            rows = cursor_obj.fetchall()
            for x in rows:
                print(x[0])
                sql2 = "SELECT UserPassword, PrivilageLevel, EmployeeID FROM Employees;"
                #args = emailname
                found_right_pass = False
                cursor_obj.execute(sql2)
                print(cursor_obj)
                valz = cursor_obj.fetchall()
                for x in range (len(valz)):
                    output = oldPassword#sha256_crypt.verify(password, valz[x][0])
                    if output == valz[x][0] and self.getUserId == valz[x][2]:
                        found_right_pass = True
                        #self.__currentUser = BookingStaff(id,name,valz[x][1])
                        primarysql = "INSERT INTO Employees (UserPassword) VALUES (%s)"
                        input = (newPassword) #Protected against sql injection
                        cursor_obj.execute(primarysql, input)
                        database.commit()
                        break
                if found_right_pass:
                    return True
                else:
                    return False



    def getUserId(self) -> int:
        return self.__userId

    def setUserId(self, input:int) -> None:
        self.__userId = input

    def getName(self) -> str:
        return self.__name

    def setName(self, input: str) -> None:
        self.__name = input

    def checkPermission(self, level: int = 1) -> bool:
        if self.__privilegesLevel >= level:
            return True
        return False


class Admin(BookingStaff):
    def generateReports() -> None:
        pass

class Manager(Admin):
    def addNewCinema(self, cinemaName, cinemaLocation, capacity) -> None:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            pushSql = "INSERT INTO Cinema (Name, CinemaLocation) VALUES (%s, %s)"
            #TO create a cinema, we need a screen, and a screen needs seats
            input = (cinemaName, cinemaLocation)
            cursor_obj.execute(pushSql, input)
            #database.commit()

            query = "SELECT CinemaId FROM Cinema ORDER BY CinemaId DESC LIMIT 1"
            cursor_obj.execute(query,)

            # Fetch the result
            newestCinema = cursor_obj.fetchone()
            for sixCinemas in range (6):
                pushSqlScreen = "INSERT INTO Screen (maxCapacity, CinemaId) VALUES (%s, %s)"
                inputScreen = (int(capacity),newestCinema[0])
                cursor_obj.execute(pushSqlScreen, inputScreen)
            database.commit()
            #Repopulate the system
            theSystem.reset()


class Booking:
    def __init__(self, _bookingReference: str, _show: Show, _tickets: list[Ticket], _bookingDate: dateTime, _totalCost: float, _customerName: str, _bookingId: int = None, _bookingStatus: str = "Active" ,_isGenerate: bool = True, _theEmployeeId: int = None):
        self.__bookingReference: str = _bookingReference
        self.__show: Show = _show
        self.__tickets: list[Ticket] = _tickets
        self.__bookingDate: dateTime = _bookingDate
        self.__totalCost: float = _totalCost
        self.__customerName: str = _customerName
        self.__bookingId: int = _bookingId
        self.__employeeId: int = None

        if _theEmployeeId == None:
            self.__employeeId = theSystem.getCurrentUser().getUserId()
        else:
            self.__employeeId = _theEmployeeId

        if _bookingStatus == 0:
            self.__bookingStatus: str = "Active"
        else:
            self.__bookingStatus: str = _bookingStatus
        # --- Potentially change below to include adding the booking Id
        if not _isGenerate:
            database = dbconnect.getConnection()
            if database.is_connected():
                cursor_obj = database.cursor()
                pushSql = "INSERT INTO BOOKING (BookingId, BookingReference, CustomerName, BookingDate, TotalCost, BookingStatus, ShowsId, EmployeeID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                input = (_bookingId, _bookingReference, _customerName, _bookingDate, _totalCost, _bookingStatus ,_show.getShowId(), self.__employeeId)
                cursor_obj.execute(pushSql, input)
                database.commit()
                self.commitCost(_totalCost, _bookingId)
            #theSystem.addBooking(self)


    def getEmployeeId(self) -> int:
        return self.__employeeId

    def setEmployeeId(self, input: int) -> None:
        self.__employeeId = input

    def commitCost(self, cost: float = 0.0, bkingId: int = 0) -> float:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            if bkingId == None:
                query = "SELECT BookingId FROM Booking ORDER BY BookingId DESC LIMIT 1"
                cursor_obj.execute(query,)
                bkingId = cursor_obj.fetchone()
            pushSql = "INSERT INTO Billings (PaymentAmount, PaymentType, BookingId) VALUES (%s, %s, %s)"
            input = (cost, 1, bkingId[0])
            cursor_obj.execute(pushSql, input)
            database.commit()
        return cost


    def cancelBooking(self) -> bool:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            print(self.__bookingId)
            primarysql = "SELECT * FROM booking WHERE BookingId = (%s)"
            cursor_obj.execute(primarysql, [self.__bookingId])
            rows = cursor_obj.fetchall()
            print(rows)
            if rows[0][3] <= dateTime.today():
                print("Not able cuz the date is invalid")
                return False
            changeSql = "UPDATE booking set BookingStatus = (%s) WHERE bookingId = (%s)"
            cursor_obj.execute(changeSql, ("Cancelled" ,self.__bookingId))
            database.commit()
            return True

    def getTotalCost(self) -> float:
        return self.__totalCost

    def customerName(self) -> str:
        return self.__customerName

    def setTotalCost(self, input: float) -> None:
        self.__totalCost = input

    def customerName(self, input: str) -> None:
        self.__customerName = input

    def getBookingReference(self) -> str:
        return self.__bookingReference

    def setBookingReference(self, input: str) -> None:
        self.__bookingReference = input

    def getShow(self) -> Show:
        return self.__show

    def setShow(self, input: Show) -> None:
        self.__show = input

    def getTickets(self) -> list[Ticket]:
        return self.__tickets

    def setTickets(self, input: list[Ticket]) -> None:
        self.__tickets = input

    def getBookingDate(self) -> dateTime:
        return self.__bookingDate

    def setBookingDate(self, input: dateTime) -> None:
        self.__bookingDate = input

    def setBookingId(self, input: int) -> None:
        self.__bookingId = input

    def getBookingId(self) -> int:
        return self.__bookingId

    def setBookingStatus(self, input: str) -> None:
        self.__bookingStatus = input
        if input == "Active":
            database = dbconnect.getConnection()
            if database.is_connected():
                cursor_obj = database.cursor()
                changeSql = "UPDATE Billings set PaymentAmount = (%s), PaymentType = (%s) WHERE BookingId = (%s)"
                cursor_obj.execute(changeSql, (self.getTotalCost(), 1, self.getBookingId()))

        elif input == "Cancelled":
            database = dbconnect.getConnection()
            if database.is_connected():
                cursor_obj = database.cursor()
                changeSql = "UPDATE Billings set PaymentAmount = (%s), PaymentType = (%s) WHERE BookingId = (%s)"
                cursor_obj.execute(changeSql, (self.getTotalCost()/2, 2, self.getBookingId()))



    def getBookingStatus(self) -> str:
        return self.__bookingStatus

    def commitToDB(self) -> bool:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            check_query = "SELECT * FROM BOOKING WHERE BookingId = %s"
            cursor_obj.execute(check_query, (self.getBookingId(),))
            result = cursor_obj.fetchone()
            if result:
                delete_query = "DELETE FROM BOOKING WHERE BookingId = %s"
                cursor_obj.execute(delete_query, (self.getBookingId(),))
                #database.commit()

            pushSql = "INSERT INTO BOOKING (BookingId, BookingReference, CustomerName, BookingDate, TotalCost, BookingStatus, ShowsId) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            input = (self.__bookingId, self.__bookingReference, self.__customerName, self.__bookingDate, self.__totalCost, self.__bookingStatus, self.__show.getShowId())
            cursor_obj.execute(pushSql, input)
            database.commit()

class CinemaSystem:
    def __init__(self) -> None:
        if not dbconnect.getConnection().is_connected():
            return False
        self.__cinemas: list[Cinema] = []
        self.__films: list[Film] = []
        self.__currentUser: BookingStaff = None
        self.__bookings: list[Booking] = []
        self.__theShows: list[Show] = []
        self.__theScreens: list[Screen] = []
        self.populateSelf()




    def addShowInDb(self, _showtime, _filmsInput, _screenInput, _inputPrice, _cinemaWhere) -> None:
        correctFilm = None
        correctScreen = None
        for x in self.getFilms():
            if x.getFilmId() == int(_filmsInput):
                correctFilm = x
                break
        for x in self.getScreens():
            if x.getScreenNumber() == int(_screenInput):
                correctScreen = x
                break
        database = dbconnect.getConnection()
        cursor_obj = database.cursor()
        if not database.is_connected():
            print("Error")
            return
        query = "SELECT ShowsId FROM Shows ORDER BY ShowsId DESC LIMIT 1"
        cursor_obj.execute(query)
        cursorFetch = cursor_obj.fetchone()
        newestShowId = 0
        if cursorFetch:
            newestShowId = int(cursorFetch[0]) + 1
        newShow = Show(_showtime, correctFilm, correctScreen, _inputPrice, int(float(_inputPrice) * 1.2), newestShowId, int(float(correctScreen.getCapacity()) * 1/3), int(float(correctScreen.getCapacity()) * 2/3) - 10, 10)
        newShow.commitToDB(_cinemaWhere)
        self.reset()

    def updateShowFromDb(self, _whichShow, _showtime, _filmsInput, _screenInput, _inputPrice, _cinemaWhere) -> None:
        correctFilm = None
        correctScreen = None
        showAsSelf = None
        correctCinemaId = None

        for x in self.getTheShows():
            if x.getShowId() == int(_whichShow):
                showAsSelf = x
                break
        for x in self.getCinemaList():
            for y in x.getShow():
                if y.getShowId() == int(_whichShow):
                    showAsSelf = y
                    correctCinemaId = x.getId()
                    break

        database = dbconnect.getConnection()
        cursor_obj = database.cursor()
        if not database.is_connected():
            print("Error")
            return
        query = "UPDATE Shows SET ShowTime = (%s), priceLowerHall = (%s), priceUpperHall = (%s), FilmId = (%s), ScreenId = (%s), CinemaId = (%s) WHERE ShowsId = (%s);"
        listInput = [showAsSelf.getShowTime(), showAsSelf.getPriceLower(), showAsSelf.getPriceUpper(), showAsSelf.getFilm().getFilmId(), showAsSelf.getScreen().getScreenNumber(), correctCinemaId, _whichShow]

        if _showtime != '':
            listInput[0] = _showtime
        if _inputPrice != '':
            listInput[1] = _inputPrice
            listInput[2] = int(float(_inputPrice) * 1.2)
        if _filmsInput != '':
            listInput[3] = _filmsInput
        if _screenInput != '':
            listInput[4] = _screenInput
        if _cinemaWhere != '':
            listInput[5] = _cinemaWhere


        for x in self.getFilms():
            if x.getFilmId() == listInput[3]:
                correctFilm = x
                break
        for x in self.getScreens():
            if x.getScreenNumber() == listInput[4]:
                correctScreen = x
                break

        inputForQuery = (listInput[0], listInput[1], listInput[2], listInput[3], listInput[4], listInput[5], listInput[6])

        cursor_obj.execute(query,  inputForQuery)
        database.commit()
        self.reset()


    def populateSelf(self) -> None:
        database = dbconnect.getConnection()
        sqlTickets = "SELECT * FROM TICKETS"
        theCursor = database.cursor()
        theCursor.execute(sqlTickets)
        listTickets = theCursor.fetchall()


        listOfActors: dict = {}
        sqlForActors = "SELECT * FROM Actors"
        actorCursor = database.cursor()
        actorCursor.execute(sqlForActors)
        actors = actorCursor.fetchall()
        for x in actors:
            if x[2] in listOfActors:
                listOfActors[x[2]].append(x[1])
            else:
                listOfActors[x[2]] = [x[1]]

        #Saving seats here before creating the cinema objects
        listOfFilms: dict = {}
        sqlForFilms = "SELECT * FROM Film"
        filmCursor = database.cursor()
        filmCursor.execute(sqlForFilms)
        films = filmCursor.fetchall()
        for x in films:
            if x[5] in listOfFilms:
                listOfFilms[x[5]].append(Film(x[1], x[2], x[3], x[4], listOfActors[x[0]], x[0]))
                self.__films.append(Film(x[1], x[2], x[3], x[4], listOfActors[x[0]], x[0]))
            else:
                listOfFilms[x[5]] = [Film(x[1], x[2], x[3], x[4], listOfActors[x[0]], x[0])]
                self.__films.append(Film(x[1], x[2], x[3], x[4], listOfActors[x[0]], x[0]))


        #Saving seats here before creating the cinema objects
        listOfSeats: dict = {}
        sqlForSeats = "SELECT * FROM Seats"
        seatCursor = database.cursor()
        seatCursor.execute(sqlForSeats)
        seats = seatCursor.fetchall()
        for x in seats:
            if x[4] in listOfSeats:
                listOfSeats[x[4]].append(Seat(x[1],int(x[2]),bool(x[3])))
            else:
                listOfSeats[x[4]] = [Seat(x[1],int(x[2]),bool(x[3]))]


        listOfShows: dict = {}
        sqlForShows = "SELECT * FROM Shows"
        ShowCursor = database.cursor()
        ShowCursor.execute(sqlForShows)
        Shows = ShowCursor.fetchall()
        for x in Shows:
            if x[6] in listOfShows:
                theFilmInput = "SELECT * FROM Film where FilmId = (%s)"
                theActorsInput = "SELECT * FROM Actors where FilmId = (%s)"
                theScreenInput = "SELECT * FROM Screen where ScreenId = (%s)"
                theFilmCursor = database.cursor()
                theFilmCursor.execute(theFilmInput, [x[4]])
                theFilm = theFilmCursor.fetchall()
                theScreenCursor = database.cursor()
                theScreenCursor.execute(theScreenInput, [x[5]])
                theScreen = theScreenCursor.fetchall()
                theActors = database.cursor()
                theActorsCursor = database.cursor()
                theActorsCursor.execute(theActorsInput, [theFilm[0][0]])
                theActors = theActorsCursor.fetchall()
                listOfShows[x[6]].append(Show(x[1],Film(theFilm[0][1], theFilm[0][2], theFilm[0][3], theFilm[0][4], [i for i in theActors], theFilm[0][0]), Screen(theScreen[0][0],theScreen[0][1], [i for i in listOfSeats[theScreen[0][0]]]), x[2], x[3], x[0], x[7], x[8], x[9]))
                self.__theShows.append(Show(x[1],Film(theFilm[0][1], theFilm[0][2], theFilm[0][3], theFilm[0][4], [i for i in theActors], theFilm[0][0]), Screen(theScreen[0][0],theScreen[0][1], [i for i in listOfSeats[theScreen[0][0]]]), x[2], x[3], x[0], x[7], x[8], x[9]))
            else:
                theFilmInput = "SELECT * FROM Film where FilmId = (%s)"
                theActorsInput = "SELECT * FROM Actors where FilmId = (%s)"
                theScreenInput = "SELECT * FROM Screen where ScreenId = (%s)"
                theFilmCursor = database.cursor()
                theFilmCursor.execute(theFilmInput, [x[4]])
                theFilm = theFilmCursor.fetchall()
                theScreenCursor = database.cursor()
                theScreenCursor.execute(theScreenInput, [x[5]])
                theScreen = theScreenCursor.fetchall()
                theActors = database.cursor()
                theActorsCursor = database.cursor()
                theActorsCursor.execute(theActorsInput, [theFilm[0][0]])
                theActors = theActorsCursor.fetchall()
                listOfShows[x[6]] = [Show(x[1],Film(theFilm[0][1], theFilm[0][2], theFilm[0][3], theFilm[0][4], [i for i in theActors], theFilm[0][0]), Screen(theScreen[0][0],theScreen[0][1], [i for i in listOfSeats[theScreen[0][0]]]), x[2], x[3], x[0], x[7], x[8], x[9])]
                self.__theShows.append(Show(x[1],Film(theFilm[0][1], theFilm[0][2], theFilm[0][3], theFilm[0][4], [i for i in theActors], theFilm[0][0]), Screen(theScreen[0][0],theScreen[0][1], [i for i in listOfSeats[theScreen[0][0]]] ), x[2], x[3], x[0], x[7], x[8], x[9]))


        #Finding the bookings aswell
        sqlForBookings = "SELECT * FROM Booking"
        bookingOutput = database.cursor()
        bookingOutput.execute(sqlForBookings)
        bookingOutput = bookingOutput.fetchall()
        for x in bookingOutput:
            theShow = None
            theTicket = []
            theSeats = None
            for value in listOfShows.values():
                for l in value:
                    if l.getShowId() == x[6]:
                        theShow = l
                        break
            for w in listTickets:
                if w[4] == x[0]:
                    for value in listOfSeats.values():
                        for l in value:
                            if l.getSeatNumber() == w[2]:
                                theSeats = value
                                break
                    if len(theTicket) > 0:
                        theTicket.append(Ticket(w[0], w[2], theSeats, w[1]))
                    else:
                        theTicket = [Ticket(w[0], w[2], theSeats, w[1])]
            self.__bookings.append(Booking(x[1], theShow, theTicket , x[3], x[4], x[2], x[0], x[5], True, x[7]))

        #Saving screens here before creating the cinema objects
        listOfScreens: dict = {}
        sqlForScreens = "SELECT * FROM SCREEN"
        secondCursor = database.cursor()
        secondCursor.execute(sqlForScreens)
        screens = secondCursor.fetchall()
        for x in screens:
            if x[2] in listOfScreens:
                if x[0] in listOfSeats:
                    listOfScreens[x[2]].append(Screen(int(x[0]),int(x[1]), [i for i in listOfSeats[x[0]]]))
                    self.__theScreens.append(Screen(int(x[0]),int(x[1]), [i for i in listOfSeats[x[0]]]))
                else:
                    listOfScreens[x[2]].append(Screen(int(x[0]),int(x[1]), []))
                    self.__theScreens.append(Screen(int(x[0]),int(x[1]), []))
            else:
                if x[0] in listOfSeats:
                    listOfScreens[x[2]] = [Screen(int(x[0]),int(x[1]), [i for i in listOfSeats[x[0]]])]
                    self.__theScreens.append(Screen(int(x[0]),int(x[1]), [i for i in listOfSeats[x[0]]]))
                else:
                    listOfScreens[x[2]] = [Screen(int(x[0]),int(x[1]), [])]
                    self.__theScreens.append(Screen(int(x[0]),int(x[1]), []))

        #Fill out all the database in here
        cursor_obj = database.cursor()
        sqlCode = "SELECT * FROM Cinema"
        cursor_obj.execute(sqlCode)
        rows = cursor_obj.fetchall()
        for x in rows:
            if x[0] in listOfShows:
                self.__cinemas.append(Cinema(x[0],x[1],x[2],listOfScreens[x[0]], listOfShows[x[0]]))
            else:
                self.__cinemas.append(Cinema(x[0],x[1],x[2],listOfScreens[x[0]], []))

    def reset(self, *args, **kwargs):
        # Reinitializing the attributes using __init__
        #self.__init__(*args, **kwargs)
        if not dbconnect.getConnection().is_connected():
            return False
        self.__cinemas: list[Cinema] = []
        self.__films: list[Film] = []
        self.__bookings: list[Booking] = []
        self.__theShows: list[Show] = []
        self.__theScreens: list[Screen] = []
        self.populateSelf()

    def login(self, id: int, name: str, password: str) -> bool:
        if self.__currentUser != None:
            return False
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            primarysql = "SELECT EmployeeID FROM Employees"
            cursor_obj.execute(primarysql)
            rows = cursor_obj.fetchall()
            for x in rows:
                if x[0] == int(id):
                    print("Email Found")
                    sql2 = "SELECT UserPassword, PrivilageLevel, EmployeeID FROM Employees;"
                    found_right_pass = False
                    cursor_obj.execute(sql2)
                    print(cursor_obj)
                    valz = cursor_obj.fetchall()
                    print(valz)
                    print(password)
                    for x in range (len(valz)):
                        output = sha256_crypt.verify(str(password), str(valz[x][0]))
                        if output and str(id) == str(valz[x][2]):
                            found_right_pass = True
                            if valz[x][1] == 1:
                                self.__currentUser = BookingStaff(id,name,valz[x][1])
                            elif valz[x][1] == 2:
                                self.__currentUser = Admin(id,name,valz[x][1])
                            else:
                                self.__currentUser = Manager(id,name,valz[x][1])
                            print(found_right_pass)
                            break
                    print("checked")
                    if found_right_pass:
                        print("Login Successful")
                        #insert login code here
                        return True
                    else:
                        return False

    def logout(self) -> None:
        self.__currentUser = None
        self.reset()

    def getCurrentUser(self):
        return self.__currentUser

    def getCinemaList(self) -> list[Cinema]:
        return self.__cinemas

    def getCinemaAtIndex(self, ind: int) -> Cinema:
        return self.__cinemas[ind]

    def getScreens(self) -> list[Screen]:
        return self.__theScreens

    def addCinema(self, idInput: int, nameInput: str, locationInput: str, screensInput: list[Screen] = []) -> None:
        #REDUNDANT FUNCITON DELETE
        self.__cinemas.append(Cinema(idInput, nameInput,locationInput,screensInput))
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            pushSql = "INSERT INTO Cinema (CinemaId, Name, CinemaLocation) VALUES (%s, %s, %s)"

            input = (idInput, nameInput, locationInput)
            cursor_obj.execute(pushSql, input)
            for x in screensInput:
                pushSql = "INSERT INTO Screen_Cinema_Relationship (ScreenId, CinemaId) VALUES (%s, %s)"
                input = ( x.getScreenNumber(),idInput)
                cursor_obj.execute(pushSql, input)
                database.commit()

    def addActors(self, actors, filmId: int = None) -> None:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            if filmId == None:
                query = "SELECT FilmId FROM Film ORDER BY FilmId DESC LIMIT 1"
                cursor_obj.execute(query)
                filmId = cursor_obj.fetchone()

            if type(actors) == list:
                for x in actors:
                    pushSql = "INSERT INTO Actors (ActorName, FilmId) VALUES (%s, %s)"
                    inputVal = (str(x), int(filmId[0]))
                    cursor_obj.execute(pushSql, inputVal)
            else:
                pushSql = "INSERT INTO Actors (ActorName, FilmId) VALUES (%s, %s)"
                inputVal = (str(actors), int(filmId[0]))
                cursor_obj.execute(pushSql, inputVal)
            database.commit()

    def addBooking(self, input: Booking) -> None:
        self.__bookings.append(input)

    def removeCinemaId(self, cinemaId: int) -> None:
        listRef = self.getCinemaList()
        for x in range(len(listRef)):
            if listRef[x].getId() == cinemaId:
                self.__cinemas.remove(self.getCinemaAtIndex())
                return

    def getCinemaByName(self, name: str) -> Cinema:
        listRef = self.getCinemaList()
        for x in range(len(listRef)):
            if listRef[x].getName() == name:
                return self.getCinemaAtIndex(x)

    def addFilm(self, _film: Film) -> None:
        self.__films.append(_film)
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            pushSql = "INSERT INTO Film (Title, Genre, duration, rating) VALUES (%s, %s, %s, %s)"

            input = (_film. getTitle(), _film.getGenre(), _film.getDuration(), _film.getRating())
            cursor_obj.execute(pushSql, input)
            database.commit()
        self.addActors(_film.getActors())
        self.reset()

    def deleteFilm(self, _filmId: int) -> None:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            delete_query = "DELETE FROM Actors WHERE FilmId = %s"
            cursor_obj.execute(delete_query, (_filmId,))
            delete_query = "DELETE FROM Shows WHERE FilmId = %s"
            cursor_obj.execute(delete_query, (_filmId,))
            delete_query = "DELETE FROM Film WHERE FilmId = %s"
            cursor_obj.execute(delete_query, (_filmId,))
            database.commit()
            self.reset()

    def deleteShow(self, _showId: int) -> None:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            delete_query = "DELETE FROM Shows WHERE ShowsId = %s"
            cursor_obj.execute(delete_query, (_showId,))
            query = "SELECT BookingId FROM Booking Where ShowsId = %s"
            cursor_obj.execute(query, (_showId,))
            bookingId = int(cursor_obj.fetchone()[0])
            delete_query = "DELETE FROM Tickets WHERE BookingId = %s"
            cursor_obj.execute(delete_query, (bookingId,))
            delete_query = "DELETE FROM Booking WHERE ShowsId = %s"
            cursor_obj.execute(delete_query, (_showId,))
            database.commit()
            self.reset()

    def getTheShows(self) -> list[Show]:
        return self.__theShows

    def getFilms(self) -> list[Film]:
        return self.__films

    def getBookings(self) -> list[Booking]:
        return self.__bookings

    def getEmployeeName(self, employeeId) -> str:
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            primarysql = "SELECT Name FROM Employees WHERE EmployeeID = (%s)"
            cursor_obj.execute(primarysql, [employeeId])
            rows = cursor_obj.fetchall()
            return rows[0]

    def getCorrectShow(self, _film, _time):
        #database = dbconnect.getConnection()
        for x in self.getTheShows():
            if x.getFilm().getTitle() == _film:
                time = str(x.getShowTime())
                if time == _time:
                    return x
        return None
        if database.is_connected():
            cursor_obj = database.cursor()
            primarysql = "SELECT * FROM booking WHERE BookingId = (%s)"
            cursor_obj.execute(primarysql, [self.__bookingId])
            rows = cursor_obj.fetchall()

    def getRevenue(self, bkId):
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            primarysql = "SELECT PaymentAmount FROM Billings WHERE BookingId = (%s)"
            cursor_obj.execute(primarysql, [bkId])
            rows = cursor_obj.fetchall()
            finalrevenue = 0
            for x in rows[0]:
                finalrevenue += x
            return finalrevenue

    def getShowRevenue(self, showID) -> float:
        totalRevenue = 0.0
        database = dbconnect.getConnection()
        if database.is_connected():
            cursor_obj = database.cursor()
            primarysql = "SELECT BookingId FROM Booking WHERE ShowsId = (%s)"
            cursor_obj.execute(primarysql, (showID,))
            rows = cursor_obj.fetchall()

            for bking in rows:
                primarysql = "SELECT PaymentAmount FROM Billings WHERE BookingId = (%s)"
                cursor_obj.execute(primarysql, bking)
                val = cursor_obj.fetchall()[0][0]
                totalRevenue += float(val)

        return totalRevenue

theSystem = CinemaSystem()

#MArk