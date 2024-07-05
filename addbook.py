from tkinter import *
from tkinter import messagebox
import sqlite3

# Connect to the SQLite database 'library.db'
con = sqlite3.connect('library.db')
cur = con.cursor()

# AddBook class for adding a new book to the library
class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200") # Set window size and position
        self.title("Add Book") # Set window title
        self.resizable(False, False)  # Disable resizing

        # top Frame
        self.topFrame = Frame(self,height=150)
        self.topFrame.pack(fill=X)
        # bottom Frame
        self.bottomFrame = Frame(self,height=600)
        self.bottomFrame.pack(fill=X)

        heading = Label(self.topFrame, text=' Add Book ', font='arial 22 bold')
        heading.place(x=290, y=60)

        # Title label and entry
        self.TitleLabel = Label(self.bottomFrame, text='Title', font='arial 12 bold')
        self.TitleLabel.place(x=40, y=40)
        self.TitleEntry = Entry(self.bottomFrame, width=30)
        self.TitleEntry.place(x=150, y=45)

        # Author label and entry
        self.AuthorLabel = Label(self.bottomFrame, text='Author', font='arial 12 bold')
        self.AuthorLabel.place(x=40, y=80)
        self.AuthorEntry = Entry(self.bottomFrame, width=30)
        self.AuthorEntry.place(x=150, y=85)

        # Year label and entry
        self.YearLabel = Label(self.bottomFrame, text='Year', font='arial 12 bold')
        self.YearLabel.place(x=40, y=120)
        self.YearEntry = Entry(self.bottomFrame, width=30)
        self.YearEntry.place(x=150, y=125)

        # ISBN label and entry
        self.ISBNLabel = Label(self.bottomFrame, text='ISBN', font='arial 12 bold')
        self.ISBNLabel.place(x=40, y=160)
        self.ISBNEntry = Entry(self.bottomFrame, width=30)
        self.ISBNEntry.place(x=150, y=165)

        # Add book button
        button = Button(self.bottomFrame, text='Add Book', command=self.addBook)
        button.place(x=270, y=200)

    # Function to add a new book to the library
    def AddBook(self):
        title = self.TitleEntry.get()
        author = self.AuthorEntry.get()
        year = self.YearEntry.get()
        isbn = self.ISBNEntry.get()

        # Check if all fields are filled
        if (title and author and year and isbn != ""):
            try:
                query = "INSERT INTO 'books' (Title, Author, Year, ISBN) VALUES (?, ?, ?, ?)"
                cur.execute(query,(title, author, year, isbn))
                con.commit()
                messagebox.showinfo("Book added successfully")
            except:
                messagebox.showerror("Error")
        else:
            messagebox.showerror("Please fill all the fields")