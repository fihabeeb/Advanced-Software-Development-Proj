import tkinter as tk
import os
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import backend

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

    def initLayout(self):
        # Configure the application's window size and title
        self.geometry('800x600')
        self.title('Horizon Interface')
        # Configure the grid layout to dynamically adjust with the window size
        for i in range(7):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        # Instantiate all pages and store them in the frames dictionary
        for F in (LoginPage, MenuPage, ListingPage, BookingPage, StaffToolsPage, ManagerToolsPage, AdminToolsPage, AdminShowsPage):
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
        # Navigate to the previous page based on the navigation history
        if len(self.history) > 1:
            self.history.pop()  # Remove the current page from history
            previousPage = self.history[-1]  # Get the name of the previous page
            self.showFrame(previousPage)  # Display the previous page

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
        self.visualizeGrid()  # Debugging visualization of the grid layout

        self.cw(ttk.Label, self, text='Login', font=('TkDefaultFont', 18, 'italic')).grid(column=3, row=1)
        self.cw(ttk.Label, self, text="Please enter your login details.").grid(column=3, row=2, sticky='n')

        self.cw(ttk.Label, self, text='Username', font=('TkDefaultFont', 11)).grid(column=2, row=2, sticky='nw')
        userField = self.cw(ttk.Entry, self)
        userField.grid(column=2, row=2, sticky='w')

        self.cw(ttk.Label, self, text='Password', font=('TkDefaultFont', 11)).grid(column=2, row=3, sticky='nw')
        passwordField = self.cw(ttk.Entry, self, show='*')
        passwordField.grid(column=2, row=3, sticky='w')

        self.cw(ttk.Label, self, text='Branch', font=('TkDefaultFont', 11)).grid(column=2, row=4, sticky='nw')
        branches = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow']
        branchVar = tk.StringVar(value=branches[0])
        branchDropdown = ttk.Combobox(self, textvariable=branchVar, values=branches, state="readonly")
        branchDropdown.grid(column=2, row=4, sticky='w')
        branchDropdown.current(0)

        btnLogin = self.cw(ttk.Button, self, text='Login', command=lambda: self.validateLogin(userField.get(), passwordField.get(), branchVar.get()))
        btnLogin.grid(column=4, row=5, sticky='e', ipady=4)

    def validateLogin(self, userId, password, branch):
        # Placeholder function for login validation
        if not backend.theSystem.login(userId, "user", password):
            return False
        print(f'Username: {userId}, Password: {password}, Branch: {branch}')
        self.parent.showFrame("MenuPage")  # Navigate to the menu page after login

class MenuPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Display the title of the page
        self.cw(ttk.Label, self, text='Horizon Management System', font=('TkDefaultFont', 18, 'italic')).grid(column=0, row=0, columnspan=7)

        # Button to navigate to the "ListingPage"
        btnCreateBooking = self.cw(ttk.Button, self, text='List Movies', command=lambda: self.parent.showFrame("ListingPage"))
        btnCreateBooking.grid(column=3, row=1, ipadx=20, ipady=10)

        # Button to navigate to the "StaffToolsPage"
        btnStaffTools = self.cw(ttk.Button, self, text='Staff Tools', command=lambda: self.parent.showFrame("StaffToolsPage"))
        btnStaffTools.grid(column=3, row=2, ipadx=20, ipady=10)

        # Button to navigate to the "ManagerToolsPage"
        btnManagerTools = self.cw(ttk.Button, self, text="Manager Tools", command=lambda: self.parent.showFrame("ManagerToolsPage"))
        btnManagerTools.grid(column=3, row=3, ipadx=20, ipady=10)

        # Button to navigate to the "AdminToolsPage"
        btnAdminTools = self.cw(ttk.Button, self, text="Admin Tools", command=lambda: self.parent.showFrame("AdminToolsPage"))
        btnAdminTools.grid(column=3, row=4, ipadx=20, ipady=10)

        # Button to navigate to the "AdminShowsPage"
        btnAdminTools = self.cw(ttk.Button, self, text="Manage Shows", command=lambda: self.parent.showFrame("AdminShowsPage"))
        btnAdminTools.grid(column=3, row=5, ipadx=20, ipady=10)

class ListingPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Variable to store selected times for each film
        self.selectedTimes = {}
        self.selectedFilm = tk.StringVar(value="")  # Variable to store the selected film's title

        # Page title
        self.cw(ttk.Label, self, text='Listings', font=('TkDefaultFont', 18, 'italic')).grid(column=0, row=0, columnspan=7)

        # Canvas for scrollable film listings
        canvas = tk.Canvas(self)
        canvas.grid(column=0, row=1, columnspan=7, rowspan=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.grid(column=6, row=1, rowspan=5, sticky="nes")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame inside the canvas to hold the film details
        filmsFrame = ttk.Frame(canvas)
        filmsFrame.grid_columnconfigure(0, weight=1)
        filmsFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

        # Dynamically adjust the size of the content to the canvas
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas.create_window((0, 0), window=filmsFrame, anchor="nw"), width=canvas.winfo_width())
        )

        # List of films to display

        films = [
            {'title': 'Spider-Man', 'score': '8.5', 'genre': 'Action', 'duration': '121 min', 'rating': 'PG-13', 'actors': 'Tobey Maguire, Kirsten Dunst'},
            {'title': 'Inception', 'score': '8.8', 'genre': 'Sci-Fi', 'duration': '148 min', 'rating': 'PG-13', 'actors': 'Leonardo DiCaprio, Joseph Gordon-Levitt'},
            {'title': 'The Dark Knight', 'score': '9.0', 'genre': 'Action', 'duration': '152 min', 'rating': 'PG-13', 'actors': 'Christian Bale, Heath Ledger'},
            {'title': 'The White Knight', 'score': '9.0', 'genre': 'Action', 'duration': '152 min', 'rating': 'PG-13', 'actors': 'Christian Bale, Heath Ledger'}
        ]

        # Create individual frames for each film
        for film in backend.theSystem.getFilms():
            frame = self.cw(ttk.LabelFrame, filmsFrame, text="")
            frame.grid(row=film.getFilmId() - 1, column=0, sticky="ew")

            # Film title
            self.cw(ttk.Label, frame, text=film.getTitle(), font=('TkDefaultFont', 14, 'italic')).grid(row=0, column=0, sticky='w')

            # Variable for the selected time of this film
            self.selectedTimes[film.getTitle()] = tk.StringVar(value="")

            # Display details of the film
            details = f"Score: None\nGenre: {film.getGenre()}\nDuration: {film.getDuration()}\nRating: {film.getRating()}"
            self.cw(ttk.Label, frame, text=details, anchor="w").grid(row=1, column=0, sticky="w")
            stringActors = ''
            for indivActor in film.getActors():
                stringActors += indivActor + ', '
            self.cw(ttk.Label, frame, text=f"Actors: {stringActors}", anchor="w").grid(row=2, column=0, sticky="w")
            self.cw(ttk.Label, frame, text='Select time', font=('TkDefaultFont', 12, 'italic')).grid(row=0, column=1, sticky='w')

            # Radio buttons for selecting times
            timesFrame = self.cw(ttk.Frame, frame)
            timesFrame.grid(row=1, column=1, sticky="ne")
            for time in ['10:00:00', '14:00:00', '18:00:00', '22:00:00']:
                ttk.Radiobutton(
                    timesFrame,
                    text=time,
                    value=time,
                    variable=self.selectedTimes[film.getTitle()]
                ).grid(row=0, column=['10:00:00', '14:00:00', '18:00:00', '22:00:00'].index(time))

        # Button to proceed with the selected film and time
        btnProceed = self.cw(ttk.Button, self, text="Proceed", command=self.proceed)
        btnProceed.grid(column=5, row=6, sticky='e', ipadx=20, ipady=10)

        # Back button
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, ipady=4)

    def proceed(self):
        # Validate the user's selection and proceed to the next page
        for film, timeVar in self.selectedTimes.items():
            if timeVar.get():
                self.selectedFilm.set(film)
                selectedTime = timeVar.get()
                print(f"Proceeding with Film: {film}, Time: {selectedTime}")
                self.parent.showFrame("BookingPage", film, selectedTime)
                return
        # Show a warning if no film and time are selected
        messagebox.showwarning("Selection Incomplete", "Please select a film and time.")

class BookingPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)

    def setParams(self, film, time):
        # Store selected film and time, initialize booking-related variables
        self.selectedDate = tk.StringVar(value="")
        self.ticketType = tk.StringVar(value="")
        self.numTickets = tk.IntVar(value=1)
        self.selectedFilm = film
        self.selectedTime = time
        self.name = "none"
        self.renderPage()  # Render the booking page with the provided parameters

    def renderPage(self):
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Page title
        self.cw(ttk.Label, self, text='Finalise Booking', font=('TkDefaultFont', 18, 'italic')).grid(column=0, row=0, columnspan=7)

        # Display selected film and time
        self.cw(ttk.Label, self, text=self.selectedFilm, font=('TkDefaultFont', 18, 'bold')).grid(column=1, row=1, sticky='nw')
        self.cw(ttk.Label, self, text=self.selectedTime, font=('TkDefaultFont', 12, 'italic')).grid(column=1, row=1, sticky='w')

        # Dropdown for selecting the date
        self.cw(ttk.Label, self, text='Select Date').grid(column=1, row=2, sticky='nw')
        valid_dates = self.generate_valid_dates()  # Generate valid booking dates
        date_dropdown = ttk.Combobox(self, textvariable=self.selectedDate, values=valid_dates, state="readonly", width=12)
        date_dropdown.grid(column=1, row=2, sticky='w')
        date_dropdown.current(0)  # Set the default value to the first option

        # Radio buttons for selecting ticket type
        self.cw(ttk.Label, self, text='Ticket Type').grid(column=1, row=3, sticky='nw')
        radio_frame = ttk.Frame(self)
        radio_frame.grid(column=1, row=3, sticky='w')
        ticket_types = ['Lower Hall', 'Upper Hall', 'Premium']
        for i, ticket in enumerate(ticket_types):
            ttk.Radiobutton(
                radio_frame,
                text=ticket,
                value=ticket,
                variable=self.ticketType
            ).grid(column=i, row=0, sticky='w')

        # Spinbox for selecting the number of tickets
        self.cw(ttk.Label, self, text='Number of Tickets').grid(column=1, row=4, sticky='nw')
        self.cw(ttk.Spinbox, self, from_=1, to=20, textvariable=self.numTickets, width=5).grid(column=1, row=4, sticky='w')

        # Input fields for user details with validation
        self.cw(ttk.Label, self, text='Name').grid(column=3, row=1, sticky='nw')
        nameField = self.cw(ttk.Entry, self, width=20)
        nameField.grid(column=3, row=1, sticky='w')
        nameField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 50), "%P"))
        self.name = nameField.get()
        self.cw(ttk.Label, self, text='Phone').grid(column=3, row=2, sticky='nw')
        phoneField = self.cw(ttk.Entry, self, width=20)
        phoneField.grid(column=3, row=2, sticky='w')
        phoneField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 15), "%P"))

        self.cw(ttk.Label, self, text='Email').grid(column=3, row=3, sticky='nw')
        emailField = self.cw(ttk.Entry, self, width=20)
        emailField.grid(column=3, row=3, sticky='w')
        emailField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 50), "%P"))

        self.cw(ttk.Label, self, text='Card Number').grid(column=3, row=4, sticky='nw')
        cardField = self.cw(ttk.Entry, self, width=20)
        cardField.grid(column=3, row=4, sticky='w')
        cardField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 16), "%P"))

        # Input fields for expiry date and CVV
        self.cw(ttk.Label, self, text='Expiry & CVV').grid(column=3, row=5, sticky='nw')
        expiry_frame = ttk.Frame(self)
        expiry_frame.grid(column=3, row=5, sticky='w')

        expiryDates = self.generate_expiry_dates()  # Generate valid expiry dates for the card
        expiryDropdown = ttk.Combobox(expiry_frame, values=expiryDates, state="readonly", width=8)
        expiryDropdown.grid(column=0, row=0, sticky='w')
        expiryDropdown.current(0)  # Set the default value to the first option

        cvvField = self.cw(ttk.Entry, expiry_frame, width=5)
        cvvField.grid(column=1, row=0, padx=10)
        cvvField.configure(validate="key", validatecommand=(self.register(lambda s: len(s) <= 3), "%P"))

        # Confirm booking button
        btnConfirm = ttk.Button(self, text="Confirm Booking", command=self.confirmBooking)
        btnConfirm.grid(column=4, row=5, sticky='e', ipadx=20, ipady=10)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, ipady=4)

    def generate_valid_dates(self):
        # Generate a list of valid booking dates (next 30 days)
        today = datetime.now().date()
        valid_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
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
        for indTickets in range (self.numTickets.get()):
            listTickets.append(backend.Ticket(None, str(self.ticketType.get()), backend.Seat(None, self.ticketType.get(), False), 0))
        #Provisionally, the self.selectedDate.get() down in getCorrectShow should be self.selectedTime
        backend.theSystem.getCurrentUser().createBooking("BkingRef", backend.theSystem.getCorrectShow(self.selectedFilm, self.selectedTime), listTickets, self.selectedDate.get(), 0, str(self.name))
        # Add the booking to the list in StaffToolsPage
        self.parent.frames["StaffToolsPage"].getBookings().append(booking)
        messagebox.showinfo("Booking Confirmed", f"Booking Details:\n\n"
                                                 f"Booking ID: {booking['id']}\n"
                                                 f"Film: {booking['film']}\n"
                                                 f"Time: {booking['time']}\n"
                                                 f"Date: {booking['date']}\n"
                                                 f"Ticket Type: {booking['ticket_type']}\n"
                                                 f"Number of Tickets: {booking['num_tickets']}\n"
                                                 f"Status: {'Active' if booking['status'] else 'Inactive'}")
        # Navigate to the Staff Tools page after confirmation
        #self.parent.showFrame("StaffToolsPage")

class StaffToolsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_booking = None  # Keeps track of the selected booking from the Treeview
        self.renderPage()  # Render the UI for Staff Tools

    def getBookings(self):
        # Returns a list of sample bookings to simulate a database or API call
        return backend.theSystem.getBookings()

    def renderPage(self):
        self.visualizeGrid()  # Debugging visualization of the grid layout

        # Page title
        self.cw(ttk.Label, self, text="Staff Tools", font=('TkDefaultFont', 18, 'italic')).grid(column=0, row=0, columnspan=7)

        # Define Treeview columns to display bookings
        columns = ("ID", "Film", "Time", "Date", "Tickets", "Status")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        tree.grid(column=0, row=1, columnspan=7, rowspan=5, sticky="nsew")

        # Configure column headings
        for col in columns:
            tree.heading(col, text=col)

        # Populate Treeview with sample bookings from `getBookings`
        bookings = self.getBookings()
        for booking in bookings:
            tree.insert("", "end", values=(
                booking.getBookingId(), booking.getShow().getFilm().getTitle(), str(booking.getShow().getShowTime()) + ":" + "00", booking.getBookingDate().date(),
                len(booking.getTickets()), booking.getBookingStatus()
            ))

        # Event handler to update selected booking when a Treeview item is selected
        def on_select(event):
            selection = tree.selection()
            if selection:
                self.selected_booking = tree.item(selection[0])["values"]

        tree.bind("<<TreeviewSelect>>", on_select)

        # Label and buttons for resuming or canceling bookings
        self.cw(ttk.Label, self, text="Resume or Cancel Booking", font=('TkDefaultFont', 14, 'italic')).grid(column=5, row=6, sticky='n', columnspan=2)
        btnResume = self.cw(ttk.Button, self, text="Resume", command=lambda: self.changeStatus(tree, 1))
        btnResume.grid(column=5, row=6, sticky="e", ipady=4)

        btnCancel = self.cw(ttk.Button, self, text="Cancel", command=lambda: self.changeStatus(tree, 0))
        btnCancel.grid(column=6, row=6, sticky="w", ipady=4)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, ipady=4)

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
                break

        # Refresh the Treeview to reflect the updated status
        for item in tree.get_children():
            tree.delete(item)
        for booking in bookings:
            tree.insert("", "end", values=(
                booking.getBookingId(), booking.getShow().getFilm().getTitle(), str(booking.getShow().getShowTime().hour) + ":" + "00", booking.getBookingDate().date(),
                len(booking.getTickets()), booking.getBookingStatus()
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
        self.cw(ttk.Label, self, text="Manager Tools", font=('TkDefaultFont', 18, 'italic')).grid(column=0, row=0, columnspan=7)

        # Treeview for displaying branch information with columns ID, Cinemas (Name), and Location
        self.tree = ttk.Treeview(self, columns=("ID", "Cinemas", "Location"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cinemas", text="Cinemas")
        self.tree.heading("Location", text="Location")
        self.tree.grid(column=0, row=1, columnspan=7, rowspan=4, sticky="nsew")

        # Populate Treeview with sample branch data
        self.populateTree()

        # Bind the Treeview selection to handle logic when a branch is selected
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)

        # Define input fields for adding new branches
        self.newBranchVar = tk.StringVar()  # Variable to store new branch name
        self.newLocationVar = tk.StringVar()  # Variable to store new branch location
        self.newCapacityVar = tk.StringVar()  # Variable to store new branch location

        self.cw(ttk.Label, self, text="Add or Remove Cinema", font=('TkDefaultFont', 14, 'italic')).grid(column=4, row=5, sticky='nw', columnspan=3)
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
        btnBack.grid(column=0, row=0, ipady=4)

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
        self.populateTree()
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
        self.cw(ttk.Label, self, text="Admin Tools", font=('TkDefaultFont', 18, 'italic')).grid(column=0, row=0, columnspan=7)

        # Treeview to display film details with defined columns
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Score", "Genre", "Duration", "Rating", "Actors"), show="headings")
        for col in ("ID", "Title", "Score", "Genre", "Duration", "Rating", "Actors"):
            self.tree.heading(col, text=col)
        self.tree.grid(column=0, row=1, columnspan=7, rowspan=4, sticky="nsew")

        # Populate Treeview with sample films
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
        self.cw(ttk.Label, self, text="Add or Remove Film", font=('TkDefaultFont', 14, 'italic')).grid(column=0, row=5, sticky='nw', columnspan=7)
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
        btnBack.grid(column=0, row=0, ipady=4)

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
            "ID": len(self.films),
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
        #backend.theSystem.addActors(self.actorsVar.get().strip().split(", "))
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
        self.cw(ttk.Label, self, text="Admin Tools", font=('TkDefaultFont', 18, 'italic')).grid(column=0, row=0, columnspan=7)
        self.cw(ttk.Label, self, text="Shows", font=('TkDefaultFont', 12)).grid(column=0, row=0, columnspan=7, sticky='s')

        # Treeview to display show details with defined columns
        self.tree = ttk.Treeview(self, columns=("showid", "showtime", "pricelower", "priceupper", "filmid", "screenid", "Film"), show="headings")
        for col in ("showid", "showtime", "pricelower", "priceupper", "filmid", "screenid", "Film"):
            self.tree.heading(col, text=col)
        self.tree.grid(column=0, row=1, columnspan=7, rowspan=4, sticky="nsew")

        # Populate Treeview with sample shows
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
        self.cw(ttk.Label, self, text="Add or Remove Show", font=('TkDefaultFont', 14, 'italic')).grid(column=0, row=5, sticky='nw', columnspan=7)
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
        btnShowupdate = self.cw(ttk.Button, self, text="Update Show", command=self.showUpdate)
        btnShowupdate.grid(column=6, row=7, sticky="sw", ipady=4)

        # Button to remove a selected show
        btnTimeUpdate = self.cw(ttk.Button, self, text="Update Time", command=self.timeUpdate)
        btnTimeUpdate.grid(column=6, row=8, sticky="nw", ipady=4)

        # Back button to navigate to the previous page
        btnBack = self.cw(ttk.Button, self, text="Back", command=self.parent.goBack)
        btnBack.grid(column=0, row=0, ipady=4)

    def populateTree(self):
        # Clear existing data from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add sample shows to the Treeview
        for show in self.shows:
            self.tree.insert("", "end", values=(show.getShowId(), show.getShowTime(), show.getPriceLower(), show.getPriceUpper(), show.getFilm().getFilmId(), show.getScreen().getScreenNumber(), show.getFilm().getTitle()))

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
            self.populateTree()
            for var in [self.showtimeVar, self.pricelowerVar, self.filmidVar, self.screenidVar, self.cinemaidVar]:
                #var.set("")  # Clear input fields
                pass
            messagebox.showinfo("Success", f"Show added successfully!")

    def timeUpdate():
        pass

if __name__ == '__main__':
    app = App()  # Create an instance of the App class
    app.mainloop()  # Run the application loop to display the interface and respond to user interaction
