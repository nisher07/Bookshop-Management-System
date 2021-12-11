from tkinter import *
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
import sqlite3


class BookShop:

    def __init__(self, root):
        db = Database()
        db.dbcon()

        self.root = root
        self.root.title("mini bookshop")
        self.root.geometry("800x500")
        self.background_image = ImageTk.PhotoImage(Image.open("image/bookbg.png"))
        self.background_label = Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0)

        # variables
        book_title = StringVar()
        author = StringVar()
        borrow_date = StringVar()
        return_date = StringVar()
        borrower_name = StringVar()
        contact_no = StringVar()

        # functions
        def winexit():
            winexit = messagebox.askyesno("confirm if you want to exit.")
            if winexit > 0:
                root.destroy()
                return

        def clear():
            self.book_title.delete(0, END)
            self.author.delete(0, END)
            self.borrow_date.delete(0, END)
            self.return_date.delete(0, END)
            self.borrower_name.delete(0, END)
            self.contact_no.delete(0, END)

        def addData():
            if len(book_title.get()) != 0:
                db.insert(book_title.get(), author.get(), borrow_date.get(), return_date.get(), borrower_name.get(),
                          contact_no.get())
                self.booklist.delete(0, END)
                self.booklist.insert(END, book_title.get(), author.get(), borrow_date.get(), return_date.get(),
                                     borrower_name.get(), contact_no.get())
            else:
                messagebox.askyesno("enter book title")

        def updateData():
            if len(book_title.get()) != 0:
                db.delete(bookdb[0])
            if len(book_title.get()) != 0:
                db.insert(book_title.get(), author.get(), borrow_date.get(), return_date.get(), borrower_name.get(),
                          contact_no.get())
                self.booklist.delete(0, END)
            self.booklist.insert(END, (
                book_title.get(), author.get(), borrow_date.get(), return_date.get(), borrower_name.get(),
                contact_no.get()))

        def displayData():
            self.booklist.delete(0, END)
            for row in db.display():
                self.booklist.insert(END, row, str(""))

        def bookdatabase(event):
            global bookdb
            searchbook = self.booklist.curselection()[0]
            bookdb = self.booklist.get(searchbook)

            self.book_title.delete(0, END)
            self.book_title.insert(END, bookdb[0])
            self.author.delete(0, END)
            self.author.insert(END, bookdb[1])
            self.borrow_date.delete(0, END)
            self.borrow_date.insert(END, bookdb[2])
            self.return_date.delete(0, END)
            self.return_date.insert(END, bookdb[3])
            self.borrower_name.delete(0, END)
            self.borrower_name.insert(END, bookdb[4])
            self.contact_no.delete(0, END)
            self.contact_no.insert(END, bookdb[5])

        def searchData():
            self.booklist.delete(0, END)
            for row in db.search(book_title.get(), author.get(), borrow_date.get(), return_date.get(),
                                 borrower_name.get(), contact_no.get()):
                self.booklist.insert(END, row, str(""))

        def deleteData():
            if len(book_title.get()) != 0:
                db.delete(bookdb[0])
                clear()
                displayData()

        # heading label
        self.heading = Label(self.root, text="BookShop Management System", font='Verdana 20 bold')
        self.heading.place(x=170, y=4)

        self.data_table = Label(self.root, text="Bookshop Info:", font='Verdana 15 bold')
        self.data_table.place(x=10, y=80)

        self.db_info = Label(self.root, text="Database Info:", font='Verdana 15 bold')
        self.db_info.place(x=434, y=80)

        # form data label
        self.book_title = Label(self.root, text="Book Title:", font='Verdana 10 bold')
        self.book_title.place(x=10, y=130)

        self.author = Label(self.root, text="Author:", font='Verdana 10 bold')
        self.author.place(x=10, y=160)

        self.borrow_date = Label(self.root, text="Borrowed Date:", font='Verdana 10 bold')
        self.borrow_date.place(x=10, y=190)

        self.return_date = Label(self.root, text="Return Date:", font='Verdana 10 bold')
        self.return_date.place(x=10, y=220)

        self.borrower_name = Label(self.root, text="Borrower Name:", font='Verdana 10 bold')
        self.borrower_name.place(x=10, y=250)

        self.contact_no = Label(self.root, text="Contact NO.:", font='Verdana 10 bold')
        self.contact_no.place(x=10, y=280)

        # entry
        self.book_title = Entry(self.root, width=40, textvariable=book_title)
        self.book_title.place(x=150, y=130)

        self.author = Entry(self.root, width=40, textvariable=author)
        self.author.place(x=150, y=160)

        self.borrow_date = Entry(self.root, width=40, textvariable=borrow_date)
        self.borrow_date.place(x=150, y=190)

        self.return_date = Entry(self.root, width=40, textvariable=return_date)
        self.return_date.place(x=150, y=220)

        self.borrower_name = Entry(self.root, width=40, textvariable=borrower_name)
        self.borrower_name.place(x=150, y=250)

        self.contact_no = Entry(self.root, width=40, textvariable=contact_no)
        self.contact_no.place(x=150, y=280)

        # scrollbar set and listbox create
        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.place(x=770, y=130, bordermode=OUTSIDE, height=172, width=15)

        self.booklist = Listbox(self.root, width=36, height=10, font='Verdana 10 bold',
                                yscrollcommand=self.scrollbar.set)
        self.booklist.bind('<<ListboxSelect>>', bookdatabase)
        self.booklist.place(x=434, y=130)
        self.scrollbar.config(command=self.booklist.yview)

        # button
        self.add = Button(self.root, text="Add Data", width=10, fg="white", bg="#DA4E90", bd=2, padx=5, pady=10,
                          font='Verdana 10 bold', command=addData)
        self.add.place(x=5, y=400)

        self.update = Button(self.root, text="Update Data", width=10, fg="white", bg="#DA4E90", bd=2, padx=5, pady=10,
                             font='Verdana 10 bold', command=updateData)
        self.update.place(x=120, y=400)

        self.display = Button(self.root, text="Display Data", width=10, fg="white", bg="#DA4E90", bd=2, padx=5, pady=10,
                              font='Verdana 10 bold', command=displayData)
        self.display.place(x=235, y=400)

        self.search = Button(self.root, text="Search Data", width=10, fg="white", bg="#DA4E90", bd=2, padx=5, pady=10,
                             font='Verdana 10 bold', command=searchData)
        self.search.place(x=350, y=400)

        self.delete = Button(self.root, text="Delete Data", width=10, fg="white", bg="#DA4E90", bd=2, padx=5, pady=10,
                             font='Verdana 10 bold', command=deleteData)
        self.delete.place(x=465, y=400)

        self.clear = Button(self.root, text="Clear Data", width=10, fg="white", bg="#DA4E90", bd=2, padx=5, pady=10,
                            font='Verdana 10 bold', command=clear)
        self.clear.place(x=580, y=400)

        self.exit = Button(self.root, text="Exit", width=9, fg="white", bg="#DA4E90", bd=2, padx=5, pady=10,
                           font='Verdana 10 bold', command=winexit)
        self.exit.place(x=695, y=400)


class Database:
    def dbcon(self):
        con = sqlite3.connect("bookshop.db")
        cur = con.cursor()
        # create table
        cur.execute(
            "CREATE TABLE IF NOT EXISTS bookinfo (id INTEGER PRIMARY KEY, Booktitle text NOT NULL, Author text NOT NULL, Bor_date text NOT NULL, Ret_date text NOT NULL, Bor_name text NOT NULL, Con_no text NOT NULL)")
        con.commit()
        con.close()

    def insert(self, Booktitle, Author, Bor_date, Ret_date, Bor_name, Con_no):
        con = sqlite3.connect("bookshop.db")
        cur = con.cursor()
        cur.execute("INSERT INTO bookinfo VALUES (NULL,?,?,?,?,?,?)",
                    (Booktitle, Author, Bor_date, Ret_date, Bor_name, Con_no))
        con.commit()
        con.close()

    def display(self):
        con = sqlite3.connect("bookshop.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM bookinfo")
        rows = cur.fetchall()
        con.close()
        return rows

    def delete(self, Booktitle):
        con = sqlite3.connect("bookshop.db")
        cur = con.cursor()
        cur.execute("DELETE FROM bookinfo WHERE id=?", (Booktitle,))
        con.commit()
        con.close()

    def search(self, Booktitle, Author, Bor_date, Ret_date, Bor_name, Con_no):
        con = sqlite3.connect("bookshop.db")
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM bookinfo WHERE Booktitle=? OR Author=? OR Bor_date=? OR Ret_date=? OR Bor_name=? OR Con_no=?",
            (Booktitle, Author, Bor_date, Ret_date, Bor_name, Con_no))
        rows = cur.fetchall()
        con.close()
        return rows

    def update(self, Booktitle="", Author="", Bor_date="", Ret_date="", Bor_name="", Con_no=""):
        con = sqlite3.connect("bookshop.db")
        cur = con.cursor()
        cur.execute("UPDATE bookinfo SET Booktitle=?, Author=? , Bor_date=? , Ret_date=? , Bor_name=? , Con_no=?",
                    (Booktitle, Author, Bor_date, Ret_date, Bor_name, Con_no))
        con.commit()
        con.close()


if __name__ == "__main__":
    root = Tk()
    app = BookShop(root)
    root.mainloop()
