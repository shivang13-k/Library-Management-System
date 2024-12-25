# Import necessary modules
import mysql.connector 
from tkinter import *
from getpass import getpass
from tkinter import messagebox

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="LIBRARY", password="admin123", database="library")
mycursor = mydb.cursor()

# Variables for user information (initialize them to None)
id1 = None
name_entry = None
pass1 = None



def add_book():
    # Create a new Tkinter window
    root = Tk()
   
    # Set the title of the window
    root.title("Library Management System")
    root.geometry("400x300")
    

    # Create labels for book details
    l = Label(root, text="Title:")
    l1 = Label(root, text="Author:")
    l2 = Label(root, text="Publisher:")
    l3 = Label(root, text="Copies:")
    l4 = Label(root, text="Floor_no:")
    l5 = Label(root, text="Rack_no:")
    l6 = Label(root, text="Shelf_no:")

    # Position labels using the grid layout
    l.grid(row=0, column=0)
    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)
    l3.grid(row=3, column=0)
    l4.grid(row=4, column=0)
    l5.grid(row=5, column=0)
    l6.grid(row=6, column=0)

    # Create entry widgets for user input
    title1 = Entry(root)
    author1 = Entry(root)
    publisher1 = Entry(root)
    copies1 = Entry(root)
    floor_no1 = Entry(root)
    rach_no1 = Entry(root)
    shelf_no1 = Entry(root)

    # Position entry widgets using the grid layout
    title1.grid(row=0, column=1)
    author1.grid(row=1, column=1)
    publisher1.grid(row=2, column=1)
    copies1.grid(row=3, column=1)
    floor_no1.grid(row=4, column=1)
    rach_no1.grid(row=5, column=1)
    shelf_no1.grid(row=6, column=1)

    # Function to save book details to the database
    def save_book():
        # Get values from entry widgets
        title = title1.get()
        author = author1.get()
        publisher = publisher1.get()
        copies = copies1.get()
        floor_no = floor_no1.get()
        rach_no = rach_no1.get()
        shelf_no = shelf_no1.get()

        # Generate book_id using Book_id function 
        book_id = Book_id(floor_no, rach_no, shelf_no)

        # Prepare data for database insertion
        data = (book_id, title, author, publisher, copies, floor_no, rach_no, shelf_no)
        
        # SQL query to insert data into the 'books' table
        query = "INSERT INTO books (book_id, book_title, author, Publisher, copies, Floor_no, Rach_no, Shelf_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        
        # Execute the query and commit changes to the database
        mycursor.execute(query, data)
        mydb.commit()
       
        
        # Show a success message to the user
        messagebox.showinfo("Success", "Book Successfully Added")
        root.destroy()

    # Create a button to save the book and position it in the window
    save_button = Button(root, text="Save Book", command=save_book)
    save_button.grid(row=7, columnspan=2, pady=10)

    # Start the Tkinter event loop
    root.mainloop()

def Book_id(Floor_no, Rach_no, Shelf_no):
    # Initialize an empty string for Book_id
    Book_id = ""

    # Determine the Book_id based on Floor_no and Rach_no
    if Floor_no == "1":
        Book_id = "A" + Rach_no
    elif Floor_no == "2":
        Book_id = "B" + Rach_no
    elif Floor_no == "3":
        Book_id = "C" + Rach_no

    # Append a letter based on Shelf_no
    if Shelf_no == "1":
        Book_id += "a"
    elif Shelf_no == "2":
        Book_id += "b"
    elif Shelf_no == "3":
        Book_id += "c"
    elif Shelf_no == "4":
        Book_id += "d"
    elif Shelf_no == "5":
        Book_id += "e"

    # Return the generated Book_id
    return Book_id
	
	
def view_books_list():
    # Fetch records from the database
    mycursor.execute("SELECT * FROM books")
    records = mycursor.fetchall()

    # Create a new Tkinter window
    view_window = Tk()
    
    view_window.title("Books List")
    view_window.geometry("500x300")

    # Create a Listbox to display records
    listbox = Listbox(view_window, width=60, height=20)
    listbox.pack(pady=20)

    # Add records to the Listbox
    for record in records:
        listbox.insert("end", record)

    # Create a Scrollbar for the Listbox
    scrollbar = Scrollbar(view_window)
    scrollbar.pack(side="right", fill="y")

    # Configure the Listbox to use the Scrollbar
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Close button to exit the view window
    close_button = Button(view_window, text="Close", command=view_window.destroy)
    close_button.pack(pady=10)

    # Start the Tkinter main loop for the view window
    view_window.mainloop()
		
				
def delete_book():
    # Create a new Tkinter window for deleting a book
    d = Tk()
    d.title("Delete Book")
    d.geometry("400x300")
   
    # Create labels for book details
    l = Label(d, text="Book_title:")
    l1 = Label(d, text="Book_id:")

    # Position labels using the grid layout
    l.grid(row=0, column=0)
    l1.grid(row=1, column=0)

    # Create entry widgets for user input
    book_title_entry = Entry(d)
    book_id_entry = Entry(d)

    # Position entry widgets using the grid layout
    book_title_entry.grid(row=0, column=1)
    book_id_entry.grid(row=1, column=1)

    # Function to delete a book from the database
    def delete():
        # Get values from entry widgets
        book_title = book_title_entry.get()
        book_id = book_id_entry.get()

        # SQL query to delete a book based on book_title and book_id
        query = "DELETE FROM books WHERE book_title = %s AND book_id = %s"
        data = (book_title, book_id)

        # Execute the delete query and commit changes to the database
        mycursor.execute(query, data)
        mydb.commit()
       

        # Get the number of deleted rows
        del_count = mycursor.rowcount

        # Check if any rows were deleted
        if del_count > 0:
            # Show success message and close the window
            messagebox.showinfo("Success", "Book Successfully Deleted")
            d.destroy()
        else:
            # Rollback changes and show an error message
            mydb.rollback()
            messagebox.showerror("Error", "Enter the correct book title and book id")

    # Create a button to delete the book and position it in the window
    delete_button = Button(d, text="Delete Book", command=delete)
    delete_button.grid(row=2, columnspan=2, pady=10)

    # Start the Tkinter event loop
    d.mainloop()
	
	
def update_book_copies(book_id,update_value):

        # Fetch current copies from the database
        query_select = "SELECT copies FROM books WHERE book_id=%s"
        data_select = (book_id,)
        mycursor.execute(query_select, data_select)
        record = mycursor.fetchone()

        # Check if the book_id is found in the database
        if record is not None:
            current_copies = record[0]

            # Calculate the new number of copies
            new_copies = current_copies + update_value

            # Update the copies in the database
            query_update = "UPDATE books SET copies=%s WHERE book_id=%s"
            data_update = (new_copies, book_id)
            mycursor.execute(query_update, data_update)
            mydb.commit()
            
        else:
            pass

    
         
	
def check_user_exists():
    # Access global variables if needed
    global root, id1

    # Get the user_id to check from the input field
    user_id_to_check = id1.get()

    # SQL query to check if the user with the given user_id exists
    check_query = "SELECT * FROM user_details WHERE user_id = %s"
    check_data = (user_id_to_check,)
    mycursor.execute(check_query, check_data)
    
    # Fetch the result of the query
    existing_user = mycursor.fetchone()

    # Check if the user exists
    if existing_user:
        # Display a message if the user exists
        messagebox.showinfo("User Exists", f"User with user_id {user_id_to_check} exists.")
        
    else:
        # Display an error message if the user does not exist
        messagebox.showerror("User Not Found", f"User with user_id {user_id_to_check} does not exist.")
        


def issue_book():
    # Access global variables if needed
    global root, id1

    # Get the user_id from the input field
    user_id = id1.get()
    

    # Create a new Tkinter window for issuing a book
    i = Tk()
   
    # Set the title of the window
    i.title("Issue Book")
    i.geometry("400x300")
   
    # Create labels for book details
    l = Label(i, text="Book_id:")
    l1 = Label(i, text="Book_title:")
    l2 = Label(i, text="Author:")
    l3 = Label(i, text="Issue_date:")

    # Position labels using the grid layout
    l.grid(row=0, column=0)
    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)
    l3.grid(row=3, column=0)

    # Create entry widgets for user input
    book_id = Entry(i)
    book_title = Entry(i)
    author = Entry(i)
    issue_date = Entry(i)

    # Position entry widgets using the grid layout
    book_id.grid(row=0, column=1)
    book_title.grid(row=1, column=1)
    author.grid(row=2, column=1)
    issue_date.grid(row=3, column=1)

    # Function to save the issued book details
    def save_issue():
        # Get values from entry widgets
        book_id_val = book_id.get()
        book_title_val = book_title.get()
        author_val = author.get()
        issue_date_val = issue_date.get()

        # Query to fetch available copies of the book
        copies_query = "SELECT copies FROM books WHERE book_id = %s"
        copies_data = (book_id_val,)
        mycursor.execute(copies_query, copies_data)
        available_copies = mycursor.fetchone()

        # Check if there are available copies to issue
        if available_copies and available_copies[0] > 0:
            # Query to insert book issuance record into 'books_issued' table
            query = "INSERT INTO books_issued (user_id, book_id, book_title, Author, issue_date) VALUES (%s, %s, %s, %s, %s)"
            data = (user_id, book_id_val, book_title_val, author_val, issue_date_val)
            mycursor.execute(query, data)
            mydb.commit()
           
            # Display a success message and update the book copies
            messagebox.showinfo("Success", f"Book Issued Successfully to user_id {user_id}")
           
            update_book_copies(book_id_val,-1)
            
            # Close the issue window after issuing the book
            i.destroy()
        else:
            # Display an info message if no available copies
            messagebox.showinfo("No Available Copies", "No available copies of the book to issue.")

    # Create a button to issue the book and position it in the window
    save_button = Button(i, text="Issue", command=save_issue)
    save_button.grid(row=4, columnspan=2, pady=10)

    # Start the Tkinter event loop
    i.mainloop()
	
	
	
def return_book():
    # Access global variables if needed
    global root, id1, mycursor, mydb
    user_id = id1.get()
    
    # Create a new Tkinter window for returning a book
    r = Tk()
   
    # Set the title of the window
    r.title("Return Book")
    r.geometry("400x300")
  
    # Create labels for book details
    l = Label(r, text="Book_id:")
    l1 = Label(r, text="Book_title:")
    l2 = Label(r, text="Return_date:")

    # Position labels using the grid layout
    l.grid(row=0, column=0)
    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)

    # Create entry widgets for user input
    book_id1 = Entry(r)
    book_title1 = Entry(r)
    return_date1 = Entry(r)

    # Position entry widgets using the grid layout
    book_id1.grid(row=0, column=1)
    book_title1.grid(row=1, column=1)
    return_date1.grid(row=2, column=1)

    # Function to save the returned book details
    def save_return():
        # Get values from entry widgets
        book_id = book_id1.get()
        book_title = book_title1.get()
        return_date = return_date1.get()

        # Query to check if the book was issued to the specified user
        check_query = "SELECT * FROM books_issued WHERE user_id = %s AND book_id = %s"
        check_data = (user_id, book_id)
        mycursor.execute(check_query, check_data)
        issued_record = mycursor.fetchone()

        # Check if the book was issued to the specified user
        if issued_record:
            # Query to insert book return record into 'books_return' table
            query = "INSERT INTO books_return (user_id, book_id, book_title, return_date) VALUES (%s, %s, %s, %s)"
            data = (user_id, book_id, book_title, return_date)
            mycursor.execute(query, data)
            mydb.commit()
            

            # Display a success message and update the book copies
            messagebox.showinfo("Success", f"Book Returned Successfully from user_id {user_id}")
            
            update_book_copies(book_id, +1)

            # Close the return window after returning the book
            r.destroy()
        else:
            # Display an info message if the book was not issued to the specified user
            messagebox.showinfo("Book Not Issued", "This book was not issued to the specified user.")

    # Create a button to return the book and position it in the window
    save_button = Button(r, text="Return", command=save_return)
    save_button.grid(row=3, columnspan=2, pady=10)

    # Start the Tkinter event loop
    r.mainloop()



		
			
def user_details():
    # Create a new Tkinter window for displaying user details
    user_details_window = Tk()
    
    # Set the title of the window
    user_details_window.title("User Details")
    user_details_window.geometry("400x300")

    # Create a scrollbar for the user listbox
    scrollbar = Scrollbar(user_details_window)
    scrollbar.pack(side="right", fill="y")

    # Create a listbox to display user details with y-scroll command linked to the scrollbar
    user_listbox = Listbox(user_details_window, yscrollcommand=scrollbar.set)
    user_listbox.pack(fill="both", expand=True)

    # Fetch user details from the database
    mycursor.execute("SELECT * FROM user_details")
    records = mycursor.fetchall()

    # Populate the listbox with user details
    for record in records:
        user_listbox.insert("end", record)

    # Configure the scrollbar to scroll the listbox
    scrollbar.config(command=user_listbox.yview)

    # Start the Tkinter event loop
    user_details_window.mainloop()

# Display a welcome message
print("Welcome to the system")
print('')
	 
	 
def prin():
    root = Tk()
    
    root.title("Library Management System")
    root.geometry("400x300")

    button = Button(root, text="To add book", command=add_book)
    button.pack(pady=10)

    button1 = Button(root, text="To issue book", command=issue_book)
    button1.pack(pady=10)

    button2 = Button(root, text="To delete book", command=delete_book)
    button2.pack(pady=10)

    button3 = Button(root, text="To return book", command=return_book)
    button3.pack(pady=10)

    button4 = Button(root, text="To view books ", command=view_books_list)
    button4.pack(pady=10)

    button5 = Button(root, text="For user details", command=user_details)
    button5.pack(pady=10)

    root.mainloop()
		
		
def student():
    root = Tk()
    
    root.title("Library Management System")
    root.geometry("400x300")

    button1 = Button(root, text="To issue book", command=issue_book)
    button1.pack(pady=10)

    button2 = Button(root, text="To return book", command=return_book)
    button2.pack(pady=10)

    button3 = Button(root, text="To view books ", command=view_books_list)
    button3.pack(pady=10)    

    root.mainloop()
		
def data():
    root = Tk()
    
    root.title("Library Management System")
    root.geometry("400x300")
    button = Button(root, text="To add book", command=add_book)
    button.pack(pady=10)

    button1 = Button(root, text="To issue book", command=issue_book)
    button1.pack(pady=10)

    button2 = Button(root, text="To delete book", command=delete_book)
    button2.pack(pady=10)

    button3 = Button(root, text="To return book", command=return_book)
    button3.pack(pady=10)

    button4 = Button(root, text="To view books ", command=view_books_list)
    button4.pack(pady=10)
    

    root.mainloop()
        
def login(records):
    # Get user inputs from entry widgets
    user_id = id1.get()
    name = name_entry.get()
    passwd = pass1.get()

    # Define predefined user credentials
    users = {'siya': 'siya20', 'sameer': 'sameer32', 'navdeep': 'navdeep12'}
    s = {'misha': '20march'}

    # Check if the entered credentials match predefined users
    if name in users and users[name] == passwd:
        # Display a success message and call the data function for regular users
        messagebox.showinfo("Login Successful", "Login Successful")
        
        data()

    elif name in s and s[name] == passwd:
        # Display a success message and call the prin function for special users
        messagebox.showinfo("Login Successful", "Login Successful")
        
        prin()

    check_query = "SELECT * FROM user_details WHERE user_id = %s"  # Fix: use user_id instead of name
    check_data = (user_id,)  # Fix: use user_id instead of name
    mycursor.execute(check_query, check_data)
    user = mycursor.fetchone()

    # Check if the user_id was found in the records
    if user is not None:
        password = user[2]
        name1= user[1]
        # Check if the entered password matches the user's password
        if passwd == password and name1 == name:
            # Display a success message and call the student function for student users
            messagebox.showinfo("Login Successful", "Login Successful")
            
            student()
        else:
            # Display an error message if the password is incorrect
            messagebox.showerror("Password Incorrect", "Password Incorrect")
            
    else:
        # Display an error message if the user_id is not found
        messagebox.showerror("User ID Not Found", "User ID not found")
        




def register():
    # Get user inputs from entry widgets
    user_id = id1.get()
    name = name_entry.get()
    passwd = pass1.get()

    # Check if the user already exists in the database
    check_query = "SELECT * FROM user_details WHERE user_id = %s"
    check_data = (user_id,)
    mycursor.execute(check_query, check_data)
    existing_user = mycursor.fetchone()

    # If user already exists, display an error message and close the window
    if existing_user:
        messagebox.showerror("Error", "User with user_id {} already exists. Please choose a different user_id.".format(user_id))
        root.destroy()
    else:
        # Insert new user into the 'user_details' table
        query = "INSERT INTO user_details (user_id, name, password) VALUES (%s, %s, %s)"
        data = (user_id, name, passwd)
        mycursor.execute(query, data)
        mydb.commit()

        # Display a success message after successful registration
        messagebox.showinfo("Success", "Sign Up Successfully")
        root.destroy()
        
        
def init():
    # Declare global variables for the main Tkinter window and entry widgets
    global root, id1, name_entry, pass1

    # Create the main Tkinter window
    root = Tk()
    root.title("Library Management System")
    root.geometry("400x300")

    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="GMAITLAB",
        passwd="admin123",
        database="library_management"
    )
    mycursor = mydb.cursor()

    # Fetch user details from the 'user_details' table
    query = "SELECT * FROM user_details"
    mycursor.execute(query)
    records = mycursor.fetchall()

    # Create labels and entry widgets for user inputs
    user_id_label = Label(root, text="User ID:")
    name_label = Label(root, text="Username:")
    password_label = Label(root, text="Password:")

    id1 = Entry(root)
    name_entry = Entry(root)
    pass1 = Entry(root, show="*")

    # Position labels and entry widgets using the grid layout
    user_id_label.grid(row=0, column=0)
    name_label.grid(row=1, column=0)
    password_label.grid(row=2, column=0)

    id1.grid(row=0, column=1)
    name_entry.grid(row=1, column=1)
    pass1.grid(row=2, column=1)

    # Create a Login button that calls the login function with fetched records
    Button(root, text="Login", command=lambda: login(records)).grid()
    
    
    # Start the Tkinter event loop
    root.mainloop()
    
  
    
def reg():
    # Declare global variables for the main Tkinter window and entry widgets
    global root, id1, name_entry, pass1

    # Create the main Tkinter window for registration
    root = Tk()
    root.title("Library Management System")
    root.geometry("400x300")

    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="GMAITLAB",
        passwd="admin123",
        database="library_management"
    )
    mycursor = mydb.cursor()

    # Fetch user details from the 'user_details' table
    query = "SELECT * FROM user_details"
    mycursor.execute(query)
    records = mycursor.fetchall()

    # Create labels and entry widgets for user registration inputs
    user_id_label = Label(root, text="User ID:")
    name_label = Label(root, text="Username:")
    password_label = Label(root, text="Password:")

    id1 = Entry(root)
    name_entry = Entry(root)
    pass1 = Entry(root, show="*")

    # Position labels and entry widgets using the grid layout
    user_id_label.grid(row=0, column=0)
    name_label.grid(row=1, column=0)
    password_label.grid(row=2, column=0)

    id1.grid(row=0, column=1)
    name_entry.grid(row=1, column=1)
    pass1.grid(row=2, column=1)

    # Create a Sign Up button that calls the register function
    Button(root, text="Sign Up", command=register).grid()
    

    # Start the Tkinter event loop for registration window
    root.mainloop()

    
   

	



def start_menu():
    # Create the main Tkinter window for the start menu
    menu = Tk()
    menu.geometry("644x700")
    menu.title("Library Management System")
    
    # Create a frame for the menu options
    f = Frame(menu, bg="black", borderwidth=5, relief=SUNKEN)
    f.pack(side=TOP, fill=X)
    
    # Create another frame for additional options
    f1 = Frame(menu, bg="black", borderwidth=5, relief="sunken")
    f1.pack(side="right", fill="y")
    
    # Display a label for choosing an option
    Label(f, text="Choose an option", font="lucida 19 bold", justify=LEFT, padx=14).pack(pady=12)

    # Create radio buttons for Sign Up, Login, and Exit options
    signup = Radiobutton(menu, text="Sign Up", command=reg, font="lucida 20 bold").pack(anchor="w")
    login = Radiobutton(menu, text="Login", command=init, font="lucida 20 bold").pack(anchor="w")
    exit_button = Radiobutton(menu, text="Exit", command=menu.destroy, font="lucida 20 bold").pack(anchor="w")
    
    # Start the Tkinter event loop for the start menu window
    menu.mainloop()
    

start_menu()