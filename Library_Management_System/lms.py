import pymysql
from pymysql.err import OperationalError
import tkinter as tk
from tkinter import messagebox, ttk

try:
    conn = pymysql.connect(
        host='localhost',
        database='robo_library',
        user='root',
        password='1234'
    )
    if conn.open:
        print('Connected to MySQL database')
        cursor = conn.cursor()

except OperationalError as e:
    print(f"Error while connecting to MySQL: {e}")
    exit(1)

def add_book():
    title = title_var.get()
    author = author_var.get()
    isbn = isbn_var.get()
    quantity = quantity_var.get()
    
    if title and author and isbn and quantity:
        try:
            sql = '''INSERT INTO books (title, author, isbn, quantity)
                     VALUES (%s, %s, %s, %s)'''
            cursor.execute(sql, (title, author, isbn, quantity))
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully.")
            fetch_books()
        except OperationalError as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error occurred: {e}")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

def fetch_books():
    for row in book_table.get_children():
        book_table.delete(row)
    try:
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        for row in rows:
            book_table.insert('', tk.END, values=row)
    except OperationalError as e:
        messagebox.showerror("Error", f"Error occurred: {e}")

def delete_book():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a book to delete.")
        return

    book_id = book_table.item(selected_item)['values'][0]
    try:
        sql = "DELETE FROM books WHERE book_id = %s"
        cursor.execute(sql, (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book deleted successfully.")
        fetch_books()
    except OperationalError as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error occurred: {e}")

def populate_fields(event):
    selected_item = book_table.selection()
    if selected_item:
        book_id = book_table.item(selected_item)['values'][0]
        title = book_table.item(selected_item)['values'][1]
        author = book_table.item(selected_item)['values'][2]
        isbn = book_table.item(selected_item)['values'][3]
        quantity = book_table.item(selected_item)['values'][4]

        title_var.set(title)
        author_var.set(author)
        isbn_var.set(isbn)
        quantity_var.set(quantity)

def update_book():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a book to update.")
        return

    book_id = book_table.item(selected_item)['values'][0]
    title = title_var.get()
    author = author_var.get()
    isbn = isbn_var.get()
    quantity = quantity_var.get()

    if title and author and isbn and quantity:
        try:
            sql = '''UPDATE books
                     SET title = %s, author = %s, isbn = %s, quantity = %s
                     WHERE book_id = %s'''
            cursor.execute(sql, (title, author, isbn, quantity, book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book updated successfully.")
            fetch_books()
        except OperationalError as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error occurred: {e}")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

def main():
    global title_var, author_var, isbn_var, quantity_var, book_table
    
    root = tk.Tk()
    root.title("Library Management System")
    
    book_frame = tk.LabelFrame(root, text="Books")
    book_frame.pack(pady=10, padx=10, fill="both", expand="yes")

    tk.Label(book_frame, text="Title:").grid(row=0, column=0, padx=10, pady=5)
    title_var = tk.StringVar()
    tk.Entry(book_frame, textvariable=title_var).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(book_frame, text="Author:").grid(row=1, column=0, padx=10, pady=5)
    author_var = tk.StringVar()
    tk.Entry(book_frame, textvariable=author_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(book_frame, text="ISBN:").grid(row=2, column=0, padx=10, pady=5)
    isbn_var = tk.StringVar()
    tk.Entry(book_frame, textvariable=isbn_var).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(book_frame, text="Quantity:").grid(row=3, column=0, padx=10, pady=5)
    quantity_var = tk.IntVar()
    tk.Entry(book_frame, textvariable=quantity_var).grid(row=3, column=1, padx=10, pady=5)

    tk.Button(book_frame, text="Add Book", command=add_book).grid(row=4, columnspan=2, pady=10)
    
    book_table_frame = tk.Frame(book_frame)
    book_table_frame.grid(row=5, columnspan=2, pady=10)
    
    columns = ("book_id", "Title", "Author", "ISBN", "Quantity")
    book_table = ttk.Treeview(book_table_frame, columns=columns, show='headings')

    for col in columns:
        book_table.heading(col, text=col)
        book_table.column(col, width=100)

    book_table.pack(side="left", fill="y")

    book_table_scroll = tk.Scrollbar(book_table_frame, orient="vertical", command=book_table.yview)
    book_table.configure(yscrollcommand=book_table_scroll.set)
    book_table_scroll.pack(side="right", fill="y")

    book_table.bind("<ButtonRelease-1>", populate_fields)

    tk.Button(book_frame, text="Update Book", command=update_book).grid(row=6, column=0, pady=10)
    tk.Button(book_frame, text="Delete Book", command=delete_book).grid(row=6, column=1, pady=10)

    fetch_books()
    root.mainloop()

if __name__ == '__main__':
    main()
