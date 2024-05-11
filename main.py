import sqlite3
from tkinter import *
from tkinter import ttk
from fpdf import FPDF
from datetime import datetime, timedelta
from PIL import ImageTk, Image
import customtkinter as ctk
from tkinter import messagebox
import random
import pandas as pd


conn = sqlite3.connect("accdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS itemdata (
    item_id INTEGER PRIMARY KEY,
    item_date text NOT NULL,
    item_name text NOT NULL,
    item_qty text NOT NULL,   
    item_cost INT NOT NULL
    
)
""")

item_id = random.randint(1000, 9999)

def add_data():
    global item_id
    item_id = random.randint(1000, 9999)
    item_date = selected_date.get()
    item_name = item_name_entry.get()
    item_qty = item_qty_entry.get()
    item_unit = selected_option.get()
    item_cost = item_cost_entry.get()
    
    if item_name and item_qty and item_cost:
        cur.execute("INSERT INTO itemdata (item_id, item_date, item_name, item_qty, item_cost) VALUES (?, ?, ?, ?, ?)",
                    (item_id, item_date, item_name, f"{item_qty} {item_unit}", f"₹{item_cost}"))
        conn.commit()
        messagebox.showinfo("Success", "Data added successfully.")
        view_data(item_date)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")


def populate_fields(event):
    global item_id  
    selected_item = tree.focus()
    if selected_item:
        item = tree.item(selected_item, "values")
        item_id = item[0]  # Store the item ID
        item_date, item_name, item_qty, item_cost = item[1], item[2], item[3], item[4]

        selected_date.set(item_date)
        item_name_entry.delete(0, END)
        item_name_entry.insert(0, item_name)
        item_qty_entry.delete(0, END)
        item_qty_entry.insert(0, item_qty.split()[0])  # Extract quantity without unit
        selected_option.set(item_qty.split()[1])  # Set selected unit in the OptionMenu
        item_cost_entry.delete(0, END)
        item_cost_entry.insert(0, item_cost)

def edit_data():
    selected_item = tree.focus()
    if selected_item:
        item_id
        item_date = selected_date.get()
        item_name = item_name_entry.get()
        item_qty = item_qty_entry.get()
        item_unit = selected_option.get()
        item_cost = item_cost_entry.get()

        print(item_id)
        
        if item_name and item_qty and item_cost:
            cur.execute("UPDATE itemdata SET item_date=?, item_name=?, item_qty=?, item_cost=? WHERE item_id=?",
                        (item_date, item_name, f"{item_qty} {item_unit}", f"₹{item_cost}", item_id))
            conn.commit()
            messagebox.showinfo("Success", "Data updated successfully.")
            view_data(item_date)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Please select a record to edit.")

def delete_data():
    selected_item = tree.focus()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
        if confirm:
            cur.execute("DELETE FROM itemdata WHERE item_id=?", (item_id,))
            conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully.")
            view_data(selected_date.get())
    else:
        messagebox.showerror("Error", "Please select a record to delete.")


def update_treeview(delta):
    current_date = datetime.strptime(selected_date.get(), "%d/%m/%Y")
    new_date = current_date + timedelta(days=delta)
    selected_date.set(new_date.strftime("%d/%m/%Y"))
    view_data(selected_date.get())

def view_data(selected_date):
    tree.delete(*tree.get_children())  # Clear existing data
    cur.execute("SELECT * FROM itemdata WHERE item_date=?", (selected_date,))
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)



root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 1200
window_height = 700

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.resizable(width=False, height=False)
root.title("Home Accounts")

root.configure(bg="white")


file_add = ImageTk.PhotoImage(Image.open("resources/Plus.png"))
file_save = ImageTk.PhotoImage(Image.open("resources/Edit.png"))
file_delete = ImageTk.PhotoImage(Image.open("resources/Recycle Bin.png"))

date_left_image = ImageTk.PhotoImage(Image.open("resources/leftV.png"))
date_right_image = ImageTk.PhotoImage(Image.open("resources/rightV.png"))

def update_date(delta):
    
    current_date = datetime.strptime(selected_date.get(), "%d/%m/%Y")
    new_date = current_date + timedelta(days=delta)
    selected_date.set(new_date.strftime("%d/%m/%Y"))
        
def get_current_date():

    global now
    now = datetime.now()
    return now.strftime("%d/%m/%Y")


selected_date = StringVar(value=get_current_date())
date_entry = Label(root, textvariable=selected_date, font=('lato', 20), fg="black", relief="flat", bg="white")
date_entry.place(x=77, y=82)
        
        
dateL = Button(master=root, image=date_left_image, highlightthickness=0, borderwidth=0, highlightbackground="white",
                       command=lambda: update_treeview(-1))
        
dateL.place(x=43, y=89)
        
        
dateR = Button(master=root,image=date_right_image, relief="flat", highlightthickness=0, borderwidth=0, highlightbackground="white",
                     command=lambda: update_treeview(1))
dateR.place(x=202, y=89)


item_name_entry = ctk.CTkEntry(master=root, width=270, height=35, 
                        fg_color="white", text_color="black", placeholder_text="Item Name")
item_name_entry.place(x=250, y=82)


item_qty_entry = ctk.CTkEntry(master=root, width=170, height=35, 
                        fg_color="white", text_color="black", placeholder_text="Quantity")
item_qty_entry.place(x=550, y=82)

selected_option = StringVar(root)
selected_option.set("gm") 

options = ["gm", "kg", "L", "ml", "pcs"]

option_menu = OptionMenu(root, selected_option, *options)
option_menu.config(width=5, height=2, background="white", foreground="black")  
option_menu.place(x=730, y=80)

item_cost_entry = ctk.CTkEntry(master=root, width=100, height=35, 
                        fg_color="white", text_color="black", placeholder_text="₹-Item Cost")
item_cost_entry.place(x=850, y=82)


button_add = Button(root, image=file_add, borderwidth=0, highlightthickness=0, command=add_data)
button_add.config(highlightbackground="white")
button_add.place(x=1000, y=82)

button_save = Button(root, image=file_save, borderwidth=0, highlightthickness=0, command=edit_data)
button_save.place(x=1050, y=82)

button_delete = Button(root, image=file_delete, borderwidth=0, highlightthickness=0, command=delete_data)
button_delete.place(x=1100, y=82)

style = ttk.Style()

# Configure the Treeview style to have a white background

tree = ttk.Treeview(root, columns=("ID", "Date", "Name", "Quantity", "Cost"))
tree.bind("<<TreeviewSelect>>", populate_fields)


tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Date", text="Date", anchor=CENTER)
tree.heading("Name", text="Name", anchor=CENTER)
tree.heading("Quantity", text="Quantity", anchor=CENTER)
tree.heading("Cost", text="Cost", anchor=CENTER)

tree.column("#0", width=0, minwidth=0, stretch=NO)
tree.column("ID", minwidth=150, width=100, stretch=False, anchor=CENTER)
tree.column("Date", minwidth=200, width=200, stretch=False, anchor=CENTER)
tree.column("Name", minwidth=100, width=300, stretch=False, anchor=CENTER)
tree.column("Quantity", minwidth=100, width=300, stretch=False, anchor=CENTER)
tree.column("Cost", minwidth=100, width=200, stretch=False, anchor=CENTER)


tree.place(x=50, y=150, height=450, width=1100)

view_data(selected_date.get())

def export_to_excel():
    data = [tree.item(item, "values") for item in tree.get_children()]
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=["ID", "Date", "Name", "Quantity", "Cost"])
    
    df.to_excel("items_data.xlsx", index=False)







excel_btn = ctk.CTkButton(master=root, text="Export to Excel", text_color="black", 
                     command=export_to_excel)
excel_btn.place(x=1004, y=642)


root.mainloop()