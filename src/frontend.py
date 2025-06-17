# SIGNATURES FROM STUDENTS: Silas Desmond(22029026), Fadil Idris Habeeb(22066955), Chi Miu Low (22066786)
import tkinter as tk
import os
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import backend
import sv_ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Define padding for widgets used throughout the app
        self.defaultPadX = 5
        self.defaultPadY = 5
        # Determine the absolute path of the current script for resource management
        self.absolutePath = os.path.dirname(os.path.abspath(__file__))
        self.iconPath = os.path.join(self.absolutePath, 'icon.ico')
        # Assign the application icon
        self.iconbitmap(self.iconPath)
        self.frames = {}  # Store all pages (frames) for easy navigation
        self.history = []  # Maintain navigation history for 'Back' functionality
        self.initLayout()  # Initialize the app's layout
        self.showFrame("LoginPage")  # Start by displaying the login page
        self.refreshStaffTools = False
        self.currentBranch = None
    


    def initLayout(self):
        # Configure the application's window size, title and theme
        self.geometry('1280x720')
        self.title('Horizon Interface')
        sv_ttk.set_theme("dark")

        # Configure the grid layout to dynamically adjust with the window size
        for i in range(7):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        # Instantiate all pages and store them in the frames dictionary
        for F in (LoginPage,):
            frame = F(self)  # Create an instance of the page (frame)
            self.frames[F.__name__] = frame  # Map the frame name to the instance
            frame.grid(row=0, column=0, columnspan=7, rowspan=7, sticky="nsew")  # Place the frame in the layout

    def initRemainingFrames(self):
        for F in (MenuPage, ListingPage, BookingPage, StaffToolsPage, ManagerToolsPage, AdminShowsPage, AdminToolsPage, AnalyticsPage):
            frame = F(self)  # Create an instance of the page (frame)
            self.frames[F.__name__] = frame  # Map the frame name to the instance
            frame.grid(row=0, column=0, columnspan=7, rowspan=7, sticky="nsew")  # Place the frame in the layout

    def showFrame(self, frameName, *args):
        # Display a specific page (frame) by its name
        frame = self.frames[frameName]
        # Pass parameters to the page if it defines a 'setParams' method
        if hasattr(frame, 'setParams'):
            frame.setParams(*args)
        frame.tkraise()  # Bring the frame to the forefront
        # Track the page in the navigation history
        if frameName not in self.history:
            self.history.append(frameName)

    def goBack(self):
        if len(self.history) > 1:
            self.history.pop()  # Remove the current page from history
            previousPage = self.history[-1]  # Get the name of the previous page
            self.showFrame(previousPage)  # Display the previous page

    def resetPages(self) -> None:
        for F in (ListingPage, BookingPage, StaffToolsPage, ManagerToolsPage, AdminShowsPage, AdminToolsPage, AnalyticsPage):
            frame = F(self) #self.frames.get(F.__name__, None)  # Retrieve the frame instance
            if frame:
                frame.grid_forget()  # Remove from layout
                frame.destroy()  # Destroy the frame
                del self.frames[F.__name__]  # Remove from dictionary

        for F in (ListingPage, BookingPage, StaffToolsPage, ManagerToolsPage, AdminShowsPage, AdminToolsPage, AnalyticsPage):
            frame = F(self)  # Create an instance of the page (frame)
            self.frames[F.__name__] = frame  # Map the frame name to the instance
            frame.grid(row=0, column=0, columnspan=7, rowspan=7, sticky="nsew")  # Place the frame in the layout

class BasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Reference to the parent App instance
        # Configure the grid layout for this page to adjust dynamically
        for i in range(7):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

    def cw(self, widgetType, *args, **kwargs):
        # Create a widget with global styling parameters and position it in the layout
        widget = widgetType(*args, **kwargs)
        widget.grid(padx=self.parent.defaultPadX, pady=self.parent.defaultPadY)  # Apply default padding
        return widget

    def visualizeGrid(self):
        return
        # Visualize the grid layout for debugging purposes (to be removed before publishing)
        for row in range(7):
            for col in range(7):
                self.cw(ttk.Label, self, text=f"({col}, {row})", relief="solid").grid(column=col, row=row, sticky="nsew")

class LoginPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.visualizeGrid()

        # Center container frame
        container = ttk.Frame(self)
        container.grid(row=0, column=0, columnspan=7, rowspan=7, sticky="nsew")

        for i in range(7):
            container.columnconfigure(i, weight=1)
            container.rowconfigure(i, weight=1)

        # Card frame
        card = ttk.LabelFrame(container, text="User Login", padding=20)
        card.grid(row=2, column=3, columnspan=1, rowspan=3, sticky="nsew", pady=10, padx=10)

        for i in range(7):
            card.rowconfigure(i, weight=1)
        card.columnconfigure(0, weight=1)

        # Title
        self.cw(ttk.Label, card, text='Login', font=('systemfixed', 18, 'bold')).grid(column=0, row=0, pady=10)
        self.cw(ttk.Label, card, text="Please enter your login details.").grid(column=0, row=1, pady=5)

        # Userid
        frame_user = ttk.Frame(card)
        frame_user.grid(column=0, row=2, pady=5, padx=20, sticky="ew")
        self.cw(ttk.Label, frame_user, text='User ID', font=('systemfixed', 11)).grid(column=0, row=0, sticky="w")
        self.userField = self.cw(ttk.Entry, frame_user)
        self.userField.grid(column=0, row=1, sticky="ew")

        # Password
        frame_pass = ttk.Frame(card)
        frame_pass.grid(column=0, row=3, pady=5, padx=20, sticky="ew")
        self.cw(ttk.Label, frame_pass, text='Password', font=('systemfixed', 11)).grid(column=0, row=0, sticky="w")
        self.passwordField = self.cw(ttk.Entry, frame_pass, show="*")
        self.passwordField.grid(column=0, row=1, sticky="ew")

        # Branch
        frame_branch = ttk.Frame(card)
        frame_branch.grid(column=0, row=4, pady=5, padx=20, sticky="ew")
        self.cw(ttk.Label, frame_branch, text='Branch', font=('systemfixed', 11)).grid(column=0, row=0, sticky="w")

        branches = backend.theSystem.getCinemaList()
        self.branchVar = tk.StringVar(value=branches[0].getName())
        branchString = []
        for indBranch in branches:
            branchString.append(indBranch.getName())
        self.branchDropdown = self.cw(ttk.Combobox, frame_branch, textvariable=self.branchVar, values=branchString, state="readonly")
        self.branchDropdown.grid(column=0, row=1, sticky="ew")
        self.branchDropdown.current(0)
        # Login button
        ttk.Button(card, text='Login', command=self.validatelogin).grid(column=0, row=5, pady=15)

    def validatelogin(self):
        if not backend.theSystem.login(self.userField.get(), "user", self.passwordField.get()):
            messagebox.showerror("Login Failed", "Invalid user id or password.")
            return
        print(f'User ID: {self.userField.get()}, Password: {self.passwordField.get()}, Branch: {self.branchVar.get()}')
        app.currentBranch = self.branchDropdown.get()
        app.initRemainingFrames()
        self.parent.showFrame("MenuPage")
        app.refreshStaffTools = True

class MenuPage(BasePage):
    def showListingsPage(self):
        self.parent.showFrame("ListingPage")
        app.frames[ListingPage.__name__].fetchFilms()

    def logout(self):
        for F in (MenuPage, ListingPage, BookingPage, StaffToolsPage, ManagerToolsPage, AdminShowsPage, AdminToolsPage, AnalyticsPage):
            frame = F(app) #self.frames.get(F.__name__, None)  # Retrieve the frame instance
            if frame:
                frame.grid_forget()  # Remove from layout
                frame.destroy()  # Destroy the frame
                del app.frames[F.__name__]  # Remove from dictionary
        # Clear the login fields
        backend.theSystem.logout()
        login_page = self.parent.frames["LoginPage"]
        login_page.userField.delete(0, tk.END)
        login_page.passwordField.delete(0, tk.END)
        # Go back to login page
        self.parent.showFrame("LoginPage")

    def __init__(self, parent):
        super().__init__(parent)
        self.visualizeGrid()

        # Create a container to center everything
        container = ttk.Frame(self)
        container.grid(row=0, column=0, columnspan=7, rowspan=7, sticky="nsew")

        for i in range(7):
            container.columnconfigure(i, weight=1)
            container.rowconfigure(i, weight=1)

        # Create the central menu "card"
        card = ttk.LabelFrame(container, text="Main Menu", padding=20)
        card.grid(row=2, column=3, columnspan=1, rowspan=3, sticky="nsew", pady=10, padx=10)

        for i in range(8):
            card.rowconfigure(i, weight=1)
        card.columnconfigure(0, weight=1)

        # Title inside the card
        ttk.Label(card, text="Horizon Management System", font=('systemfixed', 18, 'bold')).grid(column=0, row=0, pady=10)

        # Buttons for actions
        ttk.Button(card, text="List Movies", command=self.showListingsPage).grid(column=0, row=1, pady=8, ipadx=20, ipady=5)

        ttk.Button(card, text="Booking Management", command=lambda: self.parent.showFrame("StaffToolsPage")).grid(column=0, row=2, pady=8, ipadx=20, ipady=5)

        if backend.theSystem.getCurrentUser().checkPermission(3):
            ttk.Button(card, text="Cinema Management", command=lambda: self.parent.showFrame("ManagerToolsPage")).grid(column=0, row=3, pady=8, ipadx=20, ipady=5)

        if backend.theSystem.getCurrentUser().checkPermission(2):
            ttk.Button(card, text="Film Management", command=lambda: self.parent.showFrame("AdminToolsPage")).grid(column=0, row=4, pady=8, ipadx=20, ipady=5)

            ttk.Button(card, text="Show Management", command=lambda: self.parent.showFrame("AdminShowsPage")).grid(column=0, row=5, pady=8, ipadx=20, ipady=5)

            ttk.Button(card, text="Analytics", command=lambda: self.parent.showFrame("AnalyticsPage")).grid(column=0, row=6, pady=8, ipadx=20, ipady=5)

        #logout
        ttk.Button(card, text="Logout", command=self.logout).grid(column=0, row=7, pady=20, ipadx=20, ipady=5)

class ListingPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Stores selected time and film
        self.selectedTime = tk.StringVar(value="")
        self.selectedFilm = tk.StringVar(value="")

        # Page title
        self.cw(ttk.Label, self, text='Listings', font=('systemfixed', 20, 'bold')).grid(column=0, row=0, columnspan=7)

        # Canvas for scrollable film listings
        canvas = tk.Canvas(self)
        canvas.grid(column=0, row=1, columnspan=7, rowspan=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.grid(column=6, row=1, rowspan=5, sticky="nes")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame inside the canvas to hold the film details
        self.filmsFrame = ttk.Frame(canvas)
        self.filmsFrame.grid_columnconfigure(0, weight=1)
        self.filmsFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

        # Dynamically adjust the size of the content to the canvas
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas.create_window((0, 0), window=self.filmsFrame, anchor="nw"), width=canvas.winfo_width())
        )

        self.fetchFilms()



        # Button to proceed with the selected film and time
        btnProceed = self.cw(ttk.Button, self, text="Proceed", command=self.proceed)
        btnProceed.grid(column=5, row=6, sticky='e', ipadx=20, ipady=10)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, sticky="w", ipady=4)

    def fetchFilms(self):
        # Fetch films from backend
        correctCinema = None
        cinemas = backend.theSystem.getCinemaList()
        for l in cinemas:
            if l.getName() == app.currentBranch:
                correctCinema = l
                break
        for film in backend.theSystem.getFilms():
            timesForThisFilm = []

            invalidLocation = True
            listShowIds = [aShow.getShowId() for aShow in correctCinema.getShow()]
            for indivShow in backend.theSystem.getTheShows():
                if indivShow.getFilm().getFilmId() == film.getFilmId():
                    if invalidLocation and indivShow.getShowId() in listShowIds:
                        invalidLocation = False
                    timesForThisFilm.append(indivShow.getShowTime())
            if invalidLocation:
                continue

            frame = self.cw(ttk.LabelFrame, self.filmsFrame, text="")
            frame.grid(row=film.getFilmId() - 1, column=0, sticky="ew")

            # Film title
            self.cw(ttk.Label, frame, text=film.getTitle(), font=('systemfixed', 14)).grid(row=0, column=0, sticky='w')

            # Display details of the film
            details = f"Score: None\nGenre: {film.getGenre()}\nDuration: {film.getDuration()}\nRating: {film.getRating()}"
            self.cw(ttk.Label, frame, text=details, anchor="w").grid(row=1, column=0, sticky="w")

            # Actors' list as a comma-separated string
            stringActors = ', '.join(film.getActors())
            self.cw(ttk.Label, frame, text=f"Actors: {stringActors}", anchor="w").grid(row=2, column=0, sticky="w")

            # Label for selecting time
            self.cw(ttk.Label, frame, text='Select time', font=('systemfixed', 12)).grid(row=0, column=1, sticky='w')

            # Radio buttons for selecting times
            timesFrame = self.cw(ttk.Frame, frame)
            timesFrame.grid(row=1, column=1, sticky="ne")

            for time in timesForThisFilm:
                ttk.Radiobutton(
                    timesFrame,
                    text=time,
                    value=f"{film.getTitle()}|{time}",
                    variable=self.selectedTime
                ).grid(row=0, column=timesForThisFilm.index(time))


    def proceed(self):
        # Validate the user's selection and proceed to the next page
        if self.selectedTime.get():
            film, selectedTime = self.selectedTime.get().split('|')
            self.selectedFilm.set(film)
            print(f"Proceeding with Film: {film}, Time: {selectedTime}")
            app.frames[BookingPage.__name__].setParams(film,selectedTime)
            self.parent.showFrame("BookingPage", film, selectedTime)
            return
        # Show a warning if no film and time are selected
        messagebox.showwarning("Selection Incomplete", "Please select a film and time.")

class BookingPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)

    def setParams(self, film, time):
        self.selectedDate = tk.StringVar(value="")
        self.ticketType = tk.StringVar(value="")
        self.numTickets = tk.IntVar(value=1)
        self.selectedFilm = film
        self.selectedTime = time
        self.seatsLower = 0
        self.seatsUpper = 0
        self.seatsPremium = 0
        self.prices = []
        self.name = None
        self.phoneField = None
        self.emailField = None
        self.cvvField = None
        self.cardField = None
        self.renderPage()

    def renderPage(self):
        self.visualizeGrid()

        self.cw(ttk.Label, self, text='Finalise Booking', font=('systemfixed', 20, 'bold')).grid(column=0, row=0, columnspan=7)

        self.cw(ttk.Label, self, text=self.selectedFilm, font=('systemfixed', 18)).grid(column=0, row=0, sticky='s', columnspan=7)
        self.cw(ttk.Label, self, text=self.selectedTime, font=('systemfixed', 12)).grid(column=0, row=1, sticky='n', columnspan=7)


        select_frame = ttk.LabelFrame(self, text="Select Details")
        select_frame.grid(column=1, row=2, sticky='nw', padx=20, pady=10)

        customer_frame = ttk.LabelFrame(self, text="Customer Info")
        customer_frame.grid(column=1, row=3, sticky='ew', padx=20, pady=10)

        price_frame = ttk.LabelFrame(self, text="Price")
        price_frame.grid(column=4, row=2, sticky='ne', padx=20, pady=10)

        availability_frame = ttk.LabelFrame(self, text="Seat Availability")
        availability_frame.grid(column=4, row=3, sticky='ne', padx=20, pady=10)

        self.cw(ttk.Label, select_frame, text='Select Date').grid(column=0, row=0, sticky='w', pady=5)
        valid_dates = self.generate_valid_dates()
        date_dropdown = ttk.Combobox(select_frame, textvariable=self.selectedDate, values=valid_dates, state="readonly", width=15)
        date_dropdown.grid(column=1, row=0, sticky='w')
        date_dropdown.current(0)

        self.cw(ttk.Label, select_frame, text='Ticket Type').grid(column=0, row=1, sticky='w', pady=5)
        radio_frame = ttk.Frame(select_frame)
        radio_frame.grid(column=1, row=1, sticky='w')
        ticket_types = ['Lower Hall', 'Upper Hall', 'Premium']
        for i, ticket in enumerate(ticket_types):
            ttk.Radiobutton(radio_frame, text=ticket, value=ticket, variable=self.ticketType).grid(column=i, row=0, sticky='w')

        self.cw(ttk.Label, select_frame, text='Number of Tickets').grid(column=0, row=2, sticky='w', pady=5)
        self.cw(ttk.Spinbox, select_frame, from_=1, to=20, textvariable=self.numTickets, width=5).grid(column=1, row=2, sticky='w')
        
        show = backend.theSystem.getCorrectShow(self.selectedFilm, self.selectedTime)
        self.seatsLower = show.getCapacityLower()
        self.seatsUpper = show.getCapacityUpper()
        self.seatsPremium = show.getCapacityVIP()

        self.cw(ttk.Label, availability_frame, text=f"Lower Hall: {self.seatsLower}").grid(column=0, row=0, sticky='w', pady=2)
        self.cw(ttk.Label, availability_frame, text=f"Upper Hall: {self.seatsUpper}").grid(column=0, row=1, sticky='w', pady=2)
        self.cw(ttk.Label, availability_frame, text=f"Premium: {self.seatsPremium}").grid(column=0, row=2, sticky='w', pady=2)

        roundedLowerPrice = round(show.getPriceLower(),2)
        roundedUpperPrice = round(show.getPriceLower() * 1.2,2)
        roundedPremiumPrice = round(show.getPriceLower() * 1.2 * 1.2,2)
        self.prices.append(roundedLowerPrice)
        self.prices.append(roundedUpperPrice)
        self.prices.append(roundedPremiumPrice)

        self.cw(ttk.Label, price_frame, text=f"Lower hall: £{roundedLowerPrice}").grid(column=0, row=0, sticky='w', pady=2)
        self.cw(ttk.Label, price_frame, text=f"Upper hall: £{roundedUpperPrice}").grid(column=0, row=1, sticky='w', pady=2)
        self.cw(ttk.Label, price_frame, text=f"Premium hall: £{roundedPremiumPrice}").grid(column=0, row=2, sticky='w', pady=2)

        self.cw(ttk.Label, customer_frame, text='Name').grid(column=0, row=0, sticky='w')
        self.name = self.cw(ttk.Entry, customer_frame, width=20)
        self.name.grid(column=1, row=0, sticky='w', padx=5)
        self.name.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 50), "%P"))

        self.cw(ttk.Label, customer_frame, text='Email').grid(column=0, row=1, sticky='w')
        self.emailField = self.cw(ttk.Entry, customer_frame, width=20)
        self.emailField.grid(column=1, row=1, sticky='w', padx=5)
        self.emailField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 50), "%P"))

        self.cw(ttk.Label, customer_frame, text='Phone').grid(column=0, row=3, sticky='w')
        self.phoneField = self.cw(ttk.Entry, customer_frame, width=20)
        self.phoneField.grid(column=1, row=3, sticky='w', padx=5)
        self.phoneField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 15), "%P"))

        self.cw(ttk.Label, customer_frame, text='Card Number').grid(column=2, row=0, sticky='w')
        self.cardField = self.cw(ttk.Entry, customer_frame, width=20)
        self.cardField.grid(column=3, row=0, sticky='w', padx=5)
        self.cardField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 16), "%P"))
        
        self.cw(ttk.Label, customer_frame, text='Expiry Date').grid(column=2, row=1, sticky='w')
        expiryDates = self.generate_expiry_dates()
        expiryDropdown = ttk.Combobox(customer_frame, values=expiryDates, state="readonly", width=10)
        expiryDropdown.grid(column=3, row=1, sticky='w', padx=5)
        expiryDropdown.current(0)

        self.cw(ttk.Label, customer_frame, text='CVV').grid(column=4, row=0, sticky='w', padx=10)
        self.cvvField = self.cw(ttk.Entry, customer_frame, width=5)
        self.cvvField.grid(column=5, row=0, sticky='w')
        self.cvvField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 3), "%P"))

        btnConfirm = ttk.Button(self, text="Confirm Booking", command=self.confirmBooking)
        btnConfirm.grid(column=4, row=4, sticky='e', ipadx=20, ipady=10)

        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, sticky="w", ipady=4)

    def generate_valid_dates(self):
        # Generate a list of valid booking dates (next 30 days)
        today = datetime.now().date()
        valid_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        return valid_dates

    def generate_expiry_dates(self):
        # Generate a list of valid expiry dates for a credit card (next 10 years)
        current_year = datetime.now().year
        expiry_dates = [f"{month:02d}/{year % 100:02d}" for year in range(current_year, current_year + 10) for month in range(1, 13)]
        return expiry_dates

    def confirmBooking(self):
        # Ensure that a ticket type has been selected
        if not self.ticketType.get():
            messagebox.showwarning("Incomplete Selection", "Please select a ticket type.")
            return

        if not self.name.get():
            messagebox.showwarning("Incomplete Selection", "Please write customer's name.")
            return

        if not self.phoneField.get():
            messagebox.showwarning("Incomplete Selection", "Please write customer's phone number.")
            return

        if not self.cardField.get():
            messagebox.showwarning("Incomplete Selection", "Please write customer's card details.")
            return

        if not self.cvvField.get():
            messagebox.showwarning("Incomplete Selection", "Please write customer's cvv.")
            return

        if not self.emailField.get():
            messagebox.showwarning("Incomplete Selection", "Please write customer's email.")
            return
        # Create a booking dictionary based on the user's input
        booking = {
            "id": len(self.parent.frames["StaffToolsPage"].getBookings()) + 1,
            "film": self.selectedFilm,
            "time": self.selectedTime,
            "date": self.selectedDate.get(),
            "ticket_type": self.ticketType.get(),
            "num_tickets": self.numTickets.get(),
            "status": 1  # Active by default
        }
        listTickets = []
        realPrice = 0

        match booking['ticket_type']:
            case "Lower Hall":
                realPrice = self.prices[0]
                if self.seatsLower < booking['num_tickets']:
                    messagebox.showwarning("Warning","Not enough seats of specified type remaining.")
                    return
            case "Upper Hall":
                realPrice = self.prices[1]
                if self.seatsUpper < booking['num_tickets']:
                    messagebox.showwarning("Warning","Not enough seats of specified type remaining.")
                    return
            case "Premium":
                realPrice = self.prices[2]
                if self.seatsPremium < booking['num_tickets']:
                    messagebox.showwarning("Warning","Not enough seats of specified type remaining.")
                    return

        for indTickets in range (int(self.numTickets.get())):
            listTickets.append(backend.Ticket(None, str(self.ticketType.get()), backend.Seat(None, self.ticketType.get(), False), realPrice))
        #Provisionally, the self.selectedDate.get() down in getCorrectShow should be self.selectedTime

        realPrice *= booking['num_tickets']
        backend.theSystem.getCurrentUser().createBooking("Complete", backend.theSystem.getCorrectShow(self.selectedFilm, self.selectedTime), listTickets, self.selectedDate.get(), realPrice, self.name.get())
        # Add the booking to the list in StaffToolsPage
        #self.parent.frames["StaffToolsPage"].getBookings().append(booking)
        messagebox.showinfo("Booking Confirmed", f"Booking Details:\n\n"
                                                 f"Booking ID: {booking['id']}\n"
                                                 f"Film: {booking['film']}\n"
                                                 f"Time: {booking['time']}\n"
                                                 f"Date: {booking['date']}\n"
                                                 f"Ticket Type: {booking['ticket_type']}\n"
                                                 f"Number of Tickets: {booking['num_tickets']}\n"
                                                 f"Price: {realPrice}\n"
                                                 f"Status: {'Active' if booking['status'] else 'Inactive'}")
        # Navigate to the Staff Tools page after confirmation
        self.parent.showFrame("StaffToolsPage")
        app.frames[StaffToolsPage.__name__].refreshTree()




class StaffToolsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_booking = None  # Keeps track of the selected booking from the Treeview
        self.renderPage()  # Render the UI for Staff Tools

    def getBookings(self):
        # Returns a list of sample bookings to simulate a database or API call
        return backend.theSystem.getBookings()
    def refreshTree(self):
        bookings = self.getBookings()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for booking in bookings:
            self.tree.insert("", "end", values=(
                booking.getBookingId(), booking.getShow().getFilm().getTitle(), str(booking.getShow().getShowTime()) + ":" + "00", booking.getBookingDate().date(),
                len(booking.getTickets()), booking.getBookingStatus()
            ))
    def renderPage(self):
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Page title
        self.cw(ttk.Label, self, text="Booking Management", font=('systemfixed', 20, 'bold')).grid(column=0, row=0, columnspan=7)
        # Define Treeview columns to display bookings
        self.columns = ("ID", "Film", "Time", "Date", "Status")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.grid(column=0, row=1, columnspan=7, rowspan=5, sticky="nsew")

        # Configure column headings
        for col in self.columns:
            self.tree.heading(col, text=col)

        # Populate Treeview with sample bookings from `getBookings`
        bookings = self.getBookings()
        for booking in bookings:
            self.tree.insert("", "end", values=(
                booking.getBookingId(), booking.getShow().getFilm().getTitle(), str(booking.getShow().getShowTime()) + ":" + "00", booking.getBookingDate().date(),
                len(booking.getTickets()), booking.getBookingStatus()
            ))

        # Event handler to update selected booking when a Treeview item is selected
        def on_select(event):
            selection = self.tree.selection()
            if selection:
                self.selected_booking = self.tree.item(selection[0])["values"]

        self.tree.bind("<<TreeviewSelect>>", on_select)

        # Label and buttons for resuming or canceling bookings
        self.cw(ttk.Label, self, text="Resume or Cancel Booking", font=('systemfixed', 14)).grid(column=5, row=6, sticky='n', columnspan=2)
        btnResume = self.cw(ttk.Button, self, text="Resume", command=lambda: self.changeStatus(self.tree, 1))
        btnResume.grid(column=5, row=6, sticky="e", ipady=4)

        btnCancel = self.cw(ttk.Button, self, text="Cancel", command=lambda: self.changeStatus(self.tree, 0))
        btnCancel.grid(column=6, row=6, sticky="w", ipady=4)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, sticky="w", ipady=4)

    def changeStatus(self, tree, status):
        # Change the status of the selected booking
        if not self.selected_booking:
            messagebox.showwarning("No Selection", "Please select a booking first.")
            return

        # Update the status of the selected booking based on its ID
        booking_id = self.selected_booking[0]
        bookings = self.getBookings()
        for booking in bookings:
            if booking.getBookingId() == booking_id:
                booking.setBookingStatus("Active" if status == 1 else "Cancelled")
                booking.commitToDB()
                backend.theSystem.reset()
                break

        # Refresh the Treeview to reflect the updated status
        for item in tree.get_children():
            tree.delete(item)
        for booking in bookings:
            tree.insert("", "end", values=(
                booking.getBookingId(), booking.getShow().getFilm().getTitle(), str(booking.getShow().getShowTime()) + ":" + "00", booking.getBookingDate().date(),
                booking.getBookingStatus()
            ))

class ManagerToolsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        # Define default branches with IDs and UK postcode format
        self.branches = backend.theSystem.getCinemaList()
        self.renderPage()

    def renderPage(self):
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Page title
        self.cw(ttk.Label, self, text="Cinema Management", font=('systemfixed', 20, 'bold')).grid(column=0, row=0, columnspan=7)

        # Treeview for displaying branch information with columns ID, Cinemas (Name), and Location
        self.tree = ttk.Treeview(self, columns=("ID", "Cinemas", "Location"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cinemas", text="Cinemas")
        self.tree.heading("Location", text="Location")
        self.tree.grid(column=0, row=1, columnspan=7, rowspan=4, sticky="nsew")

        # Populate Treeview with sample branch data
        self.branches = backend.theSystem.getCinemaList()
        self.populateTree()

        # Bind the Treeview selection to handle logic when a branch is selected
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)

        # Define input fields for adding new branches
        self.newBranchVar = tk.StringVar()  # Variable to store new branch name
        self.newLocationVar = tk.StringVar()  # Variable to store new branch location
        self.newCapacityVar = tk.StringVar()  # Variable to store new branch location

        self.cw(ttk.Label, self, text="Add or Remove Cinema", font=('systemfixed', 14)).grid(column=4, row=5, sticky='nw', columnspan=3)
        self.cw(ttk.Label, self, text="Cinema").grid(column=3, row=5, sticky='w')

        self.cw(ttk.Entry, self, textvariable=self.newBranchVar, width=20).grid(column=3, row=5, sticky="sw", padx=5)
        self.cw(ttk.Label, self, text="Location").grid(column=4, row=5, sticky='w')
        self.cw(ttk.Entry, self, textvariable=self.newLocationVar, width=20).grid(column=4, row=5, sticky="sw", padx=5)
        self.cw(ttk.Label, self, text="Capacity").grid(column=5, row=5, sticky='w')
        self.cw(ttk.Entry, self, textvariable=self.newCapacityVar, width=20).grid(column=5, row=5, sticky="sw", padx=5)

        # Add button for creating a new branch
        btnAdd = self.cw(ttk.Button, self, text="Add", command=self.addBranch)
        btnAdd.grid(column=6, row=5, sticky="sw", ipady=4)

        # Delete button for removing an existing branch
        #btnDelete = self.cw(ttk.Button, self, text="Remove", command=self.deleteBranch)
        #btnDelete.grid(column=6, row=6, sticky="nw", ipady=4)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, sticky="w", ipady=4)

    def populateTree(self):
        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add branches to the Treeview with ID, Name, and Location columns
        for branch in self.branches:
            self.tree.insert("", "end", values=(branch.getId(), branch.getName(), branch.getLocation()))

    def onSelect(self, event):
        # Handle selection logic when a branch is clicked in the Treeview
        pass  # Currently empty as no specific action is needed on selection

    def addBranch(self):
        # Get input values for the new branch
        new_branch = self.newBranchVar.get().strip()
        new_location = self.newLocationVar.get().strip()
        new_capacity = self.newCapacityVar.get().strip()

        # Validate inputs
        if not new_branch or not new_location:
            messagebox.showwarning("Input Error", "Both Branch Name and Location must be filled.")
            return

        # Check for duplicate branch names
        if any(branch.getName() == new_branch for branch in self.branches):
            messagebox.showwarning("Duplicate Error", f"Branch '{new_branch}' already exists.")
            return

        backend.theSystem.getCurrentUser().addNewCinema(new_branch, new_location,  new_capacity)
        self.branches = backend.theSystem.getCinemaList()
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add branches to the Treeview with ID, Name, and Location columns
        for branch in self.branches:
            self.tree.insert("", "end", values=(branch.getId(), branch.getName(), branch.getLocation()))
        self.newBranchVar.set("")  # Clear input field for branch name
        self.newLocationVar.set("")  # Clear input field for branch location
        messagebox.showinfo("Success", f"Branch '{new_branch}' added successfully!")



    def deleteBranch(self):
        # Get the currently selected branch from the Treeview
        return
        selected_item = self.tree.selection()
        if selected_item:
            branch_id = self.tree.item(selected_item)["values"][0]  # Retrieve the branch ID
            self.branches = [branch for branch in self.branches if branch["ID"] != branch_id]  # Remove the branch from the list
            self.populateTree()  # Refresh the Treeview
            messagebox.showinfo("Success", f"Branch with ID '{branch_id}' deleted successfully!")
        else:
            messagebox.showwarning("Selection Error", "Please select a branch to delete.")

class AdminToolsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        # Initialize a list of preloaded sample films
        self.films = backend.theSystem.getFilms()
        self.renderPage()

    def renderPage(self):
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Page title
        self.cw(ttk.Label, self, text="Film Management", font=('systemfixed', 20, 'bold')).grid(column=0, row=0, columnspan=7)

        # Treeview to display film details with defined columns
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Score", "Genre", "Duration", "Rating", "Actors"), show="headings")
        for col in ("ID", "Title", "Score", "Genre", "Duration", "Rating", "Actors"):
            self.tree.heading(col, text=col)
        self.tree.grid(column=0, row=1, columnspan=7, rowspan=4, sticky="nsew")

        # Populate Treeview with sample films
        self.films = backend.theSystem.getFilms()
        self.populateTree()

        # Bind selection logic to the Treeview
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)

        # Define input fields for adding new films
        self.titleVar = tk.StringVar()   # Variable for film title
        self.scoreVar = tk.StringVar()   # Variable for film score
        self.genreVar = tk.StringVar()   # Variable for film genre
        self.durationVar = tk.StringVar()   # Variable for film duration
        self.ratingVar = tk.StringVar()   # Variable for film rating
        self.actorsVar = tk.StringVar()   # Variable for film actors

        # Labels and entry fields for inputting new film details
        self.cw(ttk.Label, self, text="Add or Remove Film", font=('systemfixed', 14)).grid(column=0, row=5, sticky='nw', columnspan=7)
        labels = ["Title", "Score", "Genre", "Duration", "Rating", "Actors"]
        vars = [self.titleVar, self.scoreVar, self.genreVar, self.durationVar, self.ratingVar, self.actorsVar]

        for i, label in enumerate(labels):
            self.cw(ttk.Label, self, text=label).grid(column=i, row=5, sticky="w")
            self.cw(ttk.Entry, self, textvariable=vars[i], width=20).grid(column=i, row=5, sticky="sw", padx=5)

        # Button to add a new film
        btnAdd = self.cw(ttk.Button, self, text="Add", command=self.addFilm)
        btnAdd.grid(column=6, row=5, sticky="sw", ipady=4)

        # Button to remove a selected film
        btnDelete = self.cw(ttk.Button, self, text="Remove", command=self.deleteFilm)
        btnDelete.grid(column=6, row=6, sticky="nw", ipady=4)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, sticky="w", ipady=4)

    def populateTree(self):
        # Clear existing data from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add sample films to the Treeview
        for film in self.films:
            stringActors = ''
            for indivActor in film.getActors():
                stringActors += indivActor + ', '
            self.tree.insert("", "end", values=(film.getFilmId(), film.getTitle(), "No Score", film.getGenre(), film.getDuration(), film.getRating(), stringActors))

    def onSelect(self, event):
        # Handle logic when a film is selected in the Treeview
        pass  # Placeholder for any selection-specific logic (if needed)

    def addFilm(self):
        # Create a new film dictionary from user input
        new_film = {
            "Title": self.titleVar.get().strip(),
            "Score": self.scoreVar.get().strip(),
            "Genre": self.genreVar.get().strip(),
            "Duration": self.durationVar.get().strip(),
            "Rating": self.ratingVar.get().strip(),
            "Actors": self.actorsVar.get().strip(),
        }

        # Validate all input fields to ensure completeness
        if not all(new_film.values()):
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return

        # Add the new film to the list and refresh the Treeview
        #self.films.append(new_film)
        backend.theSystem.addFilm(backend.Film(self.titleVar.get().strip(), self.genreVar.get().strip(), self.durationVar.get().strip(), self.ratingVar.get().strip(), self.actorsVar.get().strip().split(", ")) )
        self.films = backend.theSystem.getFilms()
        self.populateTree()
        for var in [self.titleVar, self.scoreVar, self.genreVar, self.durationVar, self.ratingVar, self.actorsVar]:
            var.set("")  # Clear input fields
        messagebox.showinfo("Success", f"Film '{new_film['Title']}' added successfully!")

    def deleteFilm(self):
        # Get the selected film from the Treeview
        selected_item = self.tree.selection()
        if selected_item:
            film_id = self.tree.item(selected_item)["values"][0]  # Retrieve the film's ID
            #self.films = [film for film in self.films if film.getFilmId() != film_id]  # Remove the film from the list
            backend.theSystem.deleteFilm(int(film_id))
            self.films = backend.theSystem.getFilms()
            self.populateTree()  # Refresh the Treeview
            messagebox.showinfo("Success", f"Film with ID '{film_id}' deleted successfully!")
        else:
            messagebox.showwarning("Selection Error", "Please select a film to delete.")


class AdminShowsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        # Initialize a list of preloaded sample shows
        self.shows = backend.theSystem.getTheShows()
        self.renderPage()

    def renderPage(self):
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Page title
        self.cw(ttk.Label, self, text="Show Management", font=('systemfixed', 20, 'bold')).grid(column=0, row=0, columnspan=7)
        self.cw(ttk.Label, self, text="Shows", font=('systemfixed', 12)).grid(column=0, row=0, columnspan=7, sticky='s')


        # Treeview to display show details with defined columns
        self.tree = ttk.Treeview(self, columns=("showid", "showtime", "pricelower", "priceupper", "Cinema", "screenid", "Film"  ), show="headings")
        for col in ("showid", "showtime", "pricelower", "priceupper", "Cinema", "screenid", "Film"):
            self.tree.heading(col, text=col)
        self.tree.grid(column=0, row=1, columnspan=7, rowspan=4, sticky="nsew")

        # Populate Treeview with sample shows
        self.shows = backend.theSystem.getTheShows()
        self.populateTree()

        # Bind selection logic to the Treeview
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)

        # Define input fields for adding new shows
        self.showtimeVar = tk.StringVar()
        self.pricelowerVar = tk.StringVar()
        #self.priceupperVar = tk.StringVar()
        self.filmidVar = tk.StringVar()
        self.screenidVar = tk.StringVar()
        self.cinemaidVar = tk.StringVar()

        # Labels and entry fields for inputting new show details
        self.cw(ttk.Label, self, text="Add, Update or Remove Show", font=('systemfixed', 14)).grid(column=0, row=5, sticky='nw', columnspan=7)
        labels = ["Show Time", "Price Lower", "Film ID", "Screen ID", "CinemaId"]
        vars = [self.showtimeVar, self.pricelowerVar, self.filmidVar, self.screenidVar, self.cinemaidVar]

        for i, label in enumerate(labels):
            self.cw(ttk.Label, self, text=label).grid(column=i, row=5, sticky="w")
            self.cw(ttk.Entry, self, textvariable=vars[i], width=15).grid(column=i, row=5, sticky="sw", padx=5)

        # Button to add a new show
        btnAdd = self.cw(ttk.Button, self, text="Add", command=self.addShow)
        btnAdd.grid(column=6, row=5, sticky="sw", ipady=4)

        # Button to remove a selected show
        btnDelete = self.cw(ttk.Button, self, text="Remove", command=self.deleteShow)
        btnDelete.grid(column=6, row=6, sticky="nw", ipady=4)

        # Button to add a new show
        btnShowupdate = self.cw(ttk.Button, self, text="Update", command=self.showUpdate)
        btnShowupdate.grid(column=6, row=5, sticky="se", ipady=4)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, sticky="w", ipady=4)

    def populateTree(self):
        # Clear existing data from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add sample shows to the Treeview
        correctCinema = None
        for show in self.shows:
            for indCinema in backend.theSystem.getCinemaList():
                if len(indCinema.getShow()) > 0:
                    if indCinema.getShow()[0].getShowId() == show.getShowId():
                        correctCinema = indCinema
            if correctCinema:
                self.tree.insert("", "end", values=(show.getShowId(), show.getShowTime(), show.getPriceLower(), show.getPriceUpper(), correctCinema.getName(), show.getScreen().getScreenNumber(), show.getFilm().getTitle()))

    def onSelect(self, event):
        # Handle logic when a show is selected in the Treeview
        pass  # Placeholder for any selection-specific logic (if needed)


    def addShow(self):
        # Create a new show dictionary from user input
        new_show = {
            "showtime": self.showtimeVar.get().strip(),
            "pricelower": self.pricelowerVar.get().strip(),
            "filmid": self.filmidVar.get().strip(),
            "screenid": self.screenidVar.get().strip(),
            "cinemaid": self.cinemaidVar.get().strip(),
        }

        # Validate all input fields to ensure completeness
        if not all(new_show.values()):
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return

        # Add the new show to the list and refresh the Treeview
        #self.shows.append(new_show)
        backend.theSystem.addShowInDb(new_show["showtime"], new_show["filmid"],new_show["screenid"],new_show["pricelower"], new_show["cinemaid"])
        self.shows = backend.theSystem.getTheShows()
        self.populateTree()
        for var in [self.showtimeVar, self.pricelowerVar, self.filmidVar, self.screenidVar, self.cinemaidVar]:
            var.set("")  # Clear input fields
        messagebox.showinfo("Success", f"Show added successfully!")


    def deleteShow(self):
        # Get the selected show from the Treeview
        selected_item = self.tree.selection()
        if selected_item:
            show_id = self.tree.item(selected_item)["values"][0]  # Retrieve the show's ID
            #self.shows = [show for show in self.shows if show["showid"] != show_id]  # Remove the show from the list
            backend.theSystem.deleteShow(int(show_id))
            self.shows = backend.theSystem.getTheShows()
            self.populateTree()  # Refresh the Treeview
            messagebox.showinfo("Success", f"Show with ID '{show_id}' deleted successfully!")
        else:
            messagebox.showwarning("Selection Error", "Please select a show to delete.")

    def showUpdate(self):
        # Create a new show dictionary from user input
        selected_item = self.tree.selection()
        if selected_item:
            show_id = self.tree.item(selected_item)["values"][0]
            new_show = {
                "showtime": self.showtimeVar.get().strip(),
                "pricelower": self.pricelowerVar.get().strip(),
                "filmid": self.filmidVar.get().strip(),
                "screenid": self.screenidVar.get().strip(),
                "cinemaid": self.cinemaidVar.get().strip(),
            }

            # Add the new show to the list and refresh the Treeview
            #self.shows.append(new_show)
            backend.theSystem.updateShowFromDb(int(show_id),new_show["showtime"], new_show["filmid"],new_show["screenid"],new_show["pricelower"], new_show["cinemaid"])
            self.shows = backend.theSystem.getTheShows()
            self.populateTree()
            for var in [self.showtimeVar, self.pricelowerVar, self.filmidVar, self.screenidVar, self.cinemaidVar]:
                #var.set("")  # Clear input fields
                pass
            messagebox.showinfo("Success", f"Show added successfully!")

    def timeUpdate():
        pass

class AnalyticsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.renderPage()

    def renderPage(self):
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Page title
        self.cw(ttk.Label, self, text="Analytics Page", font=('systemfixed', 20, 'bold')).grid(column=0, row=0, columnspan=7)

        # Establish treeview header, id, column header and positioning for 4 treeviews
        self.setupTreeview("Bookings by Listing", 1, ["Film ID", "Film Name", "No. of Bookings"], 0, 1, 3, 2)
        self.setupTreeview("Staff Bookings", 2, ["Staff ID", "Staff Name", "No. of Bookings"], 0, 4, 3, 2)
        self.setupTreeview("Revenue by Film", 3, ["Film ID", "Film Name", "Total Revenue"], 3, 1, 3, 2)
        self.setupTreeview("Monthly Revenue by Cinema", 4, ["Cinema ID", "Cinema Name", "Monthly Revenue"], 3, 4, 3, 2)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=1, row=0, sticky="w", ipady=4)
        self.populateData()

    def setupTreeview(self, title, tree_id, columns, start_row, start_col, colspan, rowspan):
        # Treeview header
        self.cw(ttk.Label, self, text=title, font=('systemfixed', 12)).grid(
            column=start_col, row=start_row, columnspan=colspan, sticky="s", pady=5)

        # Treeview setup
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.grid(
            column=start_col, row=start_row+1, columnspan=colspan-1, rowspan=rowspan, sticky="nsew", padx=(10, 0), pady=10)

        # Scrollbar setup
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(
            column=start_col+colspan-1, row=start_row+1, rowspan=rowspan, sticky="nsw", padx=(0, 10))

        # Treeview reference
        setattr(self, f"tree_{tree_id}", tree)

    def populateData(self):
        dictionaryOfShows = {}
        dictionaryOfEmployeeBookings = {}
        dictionaryOfFilms = {}
        dictScreens = {}
        for booking in backend.theSystem.getBookings():
            showHandle = booking.getShow()
            showId = showHandle.getShowId()
            if showId in dictionaryOfShows:
                dictionaryOfShows[showId][0] += 1
            else:
                dictionaryOfShows[showId] = [1, showHandle.getFilm().getTitle()]
            employeeId = booking.getEmployeeId()
            if employeeId in dictionaryOfEmployeeBookings:
                dictionaryOfEmployeeBookings[employeeId][0] += 1
            else:
                dictionaryOfEmployeeBookings[employeeId] = [1, backend.theSystem.getEmployeeName(employeeId)]
            film = showHandle.getFilm()
            filmId = film.getFilmId()
            if filmId in dictionaryOfFilms:
                dictionaryOfFilms[filmId][1] += backend.theSystem.getRevenue(booking.getBookingId())
            else:
                dictionaryOfFilms[filmId] = [film.getTitle(), backend.theSystem.getRevenue(booking.getBookingId())]
            screenHandle = showHandle.getScreen()
            screenId = screenHandle.getScreenNumber()
            screenRevenue = backend.theSystem.getShowRevenue(showId)
            dictScreens[screenId] = screenRevenue

        theCinemas = backend.theSystem.getCinemaList()
        dictCinemas = {}
        for val in theCinemas:
            dictCinemas[val.getId()] = [val.getName(), 0.0]
            screenIdList = []
            screens = val.getScreen()
            screenIdList = [indScreen.getScreenNumber() for indScreen in screens]
            for key in dictScreens:
                if key in screenIdList:
                    dictCinemas[val.getId()][1] += dictScreens[key]

        dictionaryOfShows = dict(sorted(dictionaryOfShows.items()))

        dictionaryOfEmployeeBookings = dict(sorted(dictionaryOfEmployeeBookings.items()))

        for key in dictionaryOfShows:
            self.tree_1.insert("", "end", values=(key, dictionaryOfShows[key][1], dictionaryOfShows[key][0]))

        for key in dictionaryOfEmployeeBookings:
            self.tree_2.insert("","end", values=(key, dictionaryOfEmployeeBookings[key][1], dictionaryOfEmployeeBookings[key][0]))

        for key in dictionaryOfFilms:
            self.tree_3.insert("","end", values=(key, dictionaryOfFilms[key][0], dictionaryOfFilms[key][1]))

        for key in dictCinemas:
            self.tree_4.insert("","end", values=(key, dictCinemas[key][0], dictCinemas[key][1]))
if __name__ == '__main__':
    app = App()  # Create an instance of the App class
    app.mainloop()  # Run the application loop to display the interface and respond to user interaction
