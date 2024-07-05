from tkinter import *
from tkinter import ttk
import sqlite3
import addbook

# Connect to the SQLite database 'library.db'
con = sqlite3.connect('library.db')
cur = con.cursor()

# Main class to handle the application
class Main(object):
    def __init__(self, master):
        self.master = master

        # Function to display the status of books
        def displayStatus(evt):
            bookCount = cur.execute("SELECT COUNT(ID) FROM Books").fetchall()
            readCount = cur.execute("SELECT COUNT(Read) FROM Books WHERE Read = 1").fetchall()
            unreadCount = cur.execute("SELECT COUNT(Read) FROM Books WHERE Read = 0").fetchall()
            print(bookCount)
            self.bookLabelCount.config(text='Total Books: ' + str(bookCount[0][0]))
            self.readLabelCount.config(text='Read Books: ' + str(readCount[0][0]))
            self.unreadLabelCount.config(text='Unread Books: ' + str(unreadCount[0][0]))
            displayBooks(self)

        # Function to display all books in the list
        def displayBooks(self):
            Books = cur.execute("SELECT * FROM Books").fetchall()
            count = 0

            # Clear the book list
            self.bookList.delete(0, END)

            # Insert books into the list
            for book in Books:
                print(book)
                self.bookList.insert(count, str(book[0]) + "-" + book[1])
                count += 1

            # Function to display detailed information about a selected book
            def bookInfo(evt):
                value = str(self.bookList.get(self.bookList.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM Books WHERE ID = ?", (id,))
                bookInfo = book.fetchall()
                print(bookInfo)

                # Clear previous details
                self.listDetails.delete(0, 'end')

                # Insert book details
                self.listDetails.insert(0, "Title: " + bookInfo[0][1])
                self.listDetails.insert(1, "Author: " + bookInfo[0][2])
                self.listDetails.insert(2, "Year: " + bookInfo[0][2])
                self.listDetails.insert(3, "ISBN: " + bookInfo[0][4])

                # Display read/unread status
                if bookInfo[0][5] == 0:
                    self.listDetails.insert(4, "Not Read")
                else:
                    self.listDetails.insert(4, "Read") 

            # Bind book selection event to bookInfo function
            self.bookList.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatus)

        # frames
        mainFrame = Frame(self.master)
        mainFrame.pack()
        # top frames
        topFrame = Frame(mainFrame, width=1350, height=70, borderwidth=2, padx=20, relief=SUNKEN)
        topFrame.pack(side = TOP, fill = X)
        # center frame
        centerFrame = Frame(mainFrame, width=1350, height=680, relief=RIDGE)
        centerFrame.pack(side = TOP)
        # center left frame
        centerLeftFrame = Frame(centerFrame, width=900, height=7000, borderwidth=2, relief=SUNKEN)
        centerLeftFrame.pack(side = LEFT)
        # center right frame
        centerRightFrame = Frame(centerFrame, width=450, height=700, borderwidth=2, relief=SUNKEN)
        centerRightFrame.pack()

        # search bar
        searchBar = LabelFrame(centerRightFrame, width=770, height=175, text='Search Book')
        searchBar.pack(fill=BOTH)
        self.searchEntry = Entry(searchBar, width=30)
        self.searchEntry.grid(row=0, column=1, padx=3, pady=10)
        self.searchButton = Button(searchBar, text='Search', font='arial 12', command=self.searchBooks)
        self.searchButton.grid(row=0, column=4, padx=20, pady=10)

        # list bar
        listBar = LabelFrame(centerRightFrame, width=700, height=175, text='Sort By')
        listBar.pack(fill=BOTH)
        self.listChoice=IntVar()
        rb1 = Radiobutton(listBar,text='All Books', var=self.listChoice, value=1)
        rb2 = Radiobutton(listBar,text='Read Books', var=self.listChoice, value=2)
        rb3 = Radiobutton(listBar,text='Unread Books', var=self.listChoice, value=3)
        rb1.grid(row=1,column=0) 
        rb2. grid (row=1, column=1)
        rb3. grid (row=1, column=2)
        listButton = Button(listBar,text='List Books', font='arial 12', command=self.bookList)
        listButton.grid(row=1, column=3, pady=10)


        # add book
        self.addBookButton = Button(topFrame, text='Add Book', compound=LEFT, font='arial 12 bold', command=self.addBook)
        self.addBookButton.pack(side=LEFT, padx=10) 

        self.tabs = ttk.Notebook(centerLeftFrame,width=900,height=660)
        self.tabs.pack()
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs) 
        self.tabs.add (self.tab1, text='Library', compound=LEFT)
        self.tabs.add(self.tab2, text='Status', compound=LEFT)

        # book list
        self.bookList = Listbox(self.tab1, width=40, height=30, font='times 12 bold')
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.bookList.grid(row=0,column=0,padx=(10,0),pady=10,sticky=N)
        self.sb.config(command=self.bookList.yview)
        self.bookList.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)
        # list details
        self.listDetails = Listbox(self.tab1, width=80, height=30, font='times 12 bold')
        self.listDetails.grid(row=0, column=1, padx=(10,0), pady=10, sticky=N)

        # status
        self.bookLabelCount = Label(self.tab2, text="", font='verdana 14 bold')
        self.bookLabelCount.grid(row=0)
        self.readLabelCount = Label(self.tab2,text="", font='verdana 14 bold')
        self.readLabelCount.grid(row=1)
        self.unreadLabelCount = Label(self.tab2, text="", font='verdana 14 bold')
        self.unreadLabelCount.grid(row=2)


        # functions
        displayBooks(self)
        displayStatus(self)

    # Function to open the add book window
    def addBook(self):
        add = addbook.AddBook()

    # Function to search books
    def searchBooks(self):
        value = self.searchEntry.get()
        search = cur.execute("SELECT * FROM Books WHERE Title LIKE ?", ('%' + value + '%',)).fetchall()
        print(search)
        self.bookList.delete(0, END)
        count = 0

        for book in search:
            self.bookList.insert(count, str(book[0]) + "-" + book[1])
            count += 1

    # Function to list books
    def bookList(self):
        value = self.listChoice.get()
        if value == 1:
            allBooks = cur.execute("SELECT * FROM Books").fetchall()
            self.bookList.delete(0, END)
            count = 0

            for book in allBooks:
                self.bookList.insert(count, str(book[0]) + "-" + book[1])
                count += 1

        elif value == 2:
            readBooks = cur.execute("SELECT * FROM Books WHERE Read = ?", (1,)).fetchall()
            self.bookList.delete(0, END)
            count = 0

            for book in readBooks:
                self.bookList.insert(count, str(book[0]) + "-" + book[1])
                count += 1

        else:
            unreadBooks = cur.execute("SELECT * FROM Books WHERE Read = ?", (0,)).fetchall()
            self.bookList.delete(0, END)
            count = 0

            for book in unreadBooks:
                self.bookList.insert(count, str(book[0]) + "-" + book[1])
                count += 1

# Main function to run the application
def main():
    root = Tk()
    app = Main(root)
    root.title("My Library")
    root.geometry("1350x750+350+200")
    root.mainloop()

if __name__ == '__main__':
    main()

    