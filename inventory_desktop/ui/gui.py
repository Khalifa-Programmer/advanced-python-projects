
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import csv
from services.inventory_service import InventoryService
from database.models import create_tables
import os

# ألوان عصرية
BG_COLOR = "#f5f6fa"
HEADER_COLOR = "#4078c0"
BTN_COLOR = "#2ecc71"
BTN_TEXT_COLOR = "#fff"
LISTBOX_BG = "#ecf0f1"
FONT = ("Segoe UI", 12)

create_tables()
inventory = InventoryService()


window = Tk()
window.title("Inventory System")
# حساب مركز الشاشة
window_width = 900
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.configure(bg=BG_COLOR)

# Header
header = Frame(window, bg=HEADER_COLOR, height=60)
header.pack(fill=X)
Label(header, text="Inventory Management", bg=HEADER_COLOR, fg="white", font=("Segoe UI", 20, "bold"), pady=10).pack(side=LEFT, padx=20)

# حقول الإدخال
form = Frame(window, bg=BG_COLOR)
form.pack(pady=20)
Label(form, text="Name", bg=BG_COLOR, font=FONT).grid(row=0, column=0, padx=10, pady=5)
Label(form, text="Quantity", bg=BG_COLOR, font=FONT).grid(row=0, column=2, padx=10, pady=5)
Label(form, text="Price", bg=BG_COLOR, font=FONT).grid(row=1, column=0, padx=10, pady=5)

name_var = StringVar()
quantity_var = StringVar()
price_var = StringVar()

Entry(form, textvariable=name_var, font=FONT, width=18).grid(row=0, column=1, padx=10)
Entry(form, textvariable=quantity_var, font=FONT, width=10).grid(row=0, column=3, padx=10)
Entry(form, textvariable=price_var, font=FONT, width=18).grid(row=1, column=1, padx=10)

# Listbox

list_frame = Frame(window, bg=BG_COLOR)
list_frame.pack(pady=10)
listbox = Listbox(list_frame, width=80, height=12, font=("Consolas", 12), bg=LISTBOX_BG, bd=0, highlightthickness=1, relief=SOLID)
listbox.pack(side=LEFT, padx=10)
scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# تحميل أيقونات (ضع صور PNG في ui/icons)
def load_icon(name):
    path = os.path.join(os.path.dirname(__file__), "icons", name)
    if os.path.exists(path):
        return PhotoImage(file=path)
    return None

icon_view = load_icon("view.png")
icon_add = load_icon("add.png")
icon_update = load_icon("update.png")
icon_delete = load_icon("delete.png")
icon_csv = load_icon("csv.png")

# وظائف CRUD
def view_data():
    listbox.delete(0, END)
    # تنسيق الجدول
    header = f"{'ID':<5} {'Name':<20} {'Quantity':<10} {'Price':<10}"
    listbox.insert(END, header)
    listbox.insert(END, "="*55)
    for row in inventory.view_products():
        line = f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<10.2f}"
        listbox.insert(END, line)

def add_data():
    name = name_var.get().strip()
    if not name:
        messagebox.showerror("Error", "Name cannot be empty.")
        return
    # فحص التكرار
    for prod in inventory.view_products():
        if prod[1].lower() == name.lower():
            messagebox.showerror("Error", "Product already exists.")
            return
    try:
        quantity = int(quantity_var.get())
        price = float(price_var.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid quantity and price.")
        return
    inventory.add_product(name, quantity, price)
    view_data()
    messagebox.showinfo("Success", "Product added successfully.")

def delete_data():
    selected = listbox.get(ACTIVE)
    if not selected:
        messagebox.showerror("Error", "Please select a product to delete.")
        return
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product: {selected[1]}?")
    if confirm:
        inventory.delete_product(selected[0])
        view_data()
        messagebox.showinfo("Deleted", "Product deleted successfully.")

def update_data():
    selected_idx = listbox.curselection()
    if not selected_idx or selected_idx[0] < 2:
        messagebox.showerror("Error", "Please select a product to update.")
        return
    selected = listbox.get(selected_idx)
    # استخراج القيم من السطر
    parts = selected.split()
    pid = int(parts[0])
    old_name = parts[1]
    old_quantity = parts[2]
    old_price = parts[3]

    # نافذة منبثقة للتعديل
    edit_win = Toplevel(window)
    edit_win.title("Edit Product")
    edit_win.geometry("350x220")
    Label(edit_win, text=f"ID: {pid}", font=FONT).pack(pady=8)
    Label(edit_win, text="Name:", font=FONT).pack()
    name_entry = Entry(edit_win, font=FONT)
    name_entry.pack()
    name_entry.insert(0, old_name)
    Label(edit_win, text="Quantity:", font=FONT).pack()
    quantity_entry = Entry(edit_win, font=FONT)
    quantity_entry.pack()
    quantity_entry.insert(0, old_quantity)
    Label(edit_win, text="Price:", font=FONT).pack()
    price_entry = Entry(edit_win, font=FONT)
    price_entry.pack()
    price_entry.insert(0, old_price)

    def save_edit():
        try:
            new_quantity = int(quantity_entry.get())
            new_price = float(price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price.")
            return
        inventory.update_product(pid, new_quantity, new_price)
        view_data()
        messagebox.showinfo("Success", "Product updated successfully.")
        edit_win.destroy()

    Button(edit_win, text="Save", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=FONT, command=save_edit).pack(pady=10)

def export_csv():
    data = inventory.view_products()
    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Quantity", "Price"])
        writer.writerows(data)
    messagebox.showinfo("Success", "CSV Exported")

# أزرار مع أيقونات وتصميم عصري

btn_frame = Frame(window, bg=BG_COLOR)
btn_frame.pack(pady=30)

Button(btn_frame, text="View", image=icon_view, compound=LEFT, font=FONT, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=view_data, bd=0, relief=RIDGE, padx=18, pady=10).pack(side=LEFT, padx=18)
Button(btn_frame, text="Add", image=icon_add, compound=LEFT, font=FONT, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=add_data, bd=0, relief=RIDGE, padx=18, pady=10).pack(side=LEFT, padx=18)
Button(btn_frame, text="Update", image=icon_update, compound=LEFT, font=FONT, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=update_data, bd=0, relief=RIDGE, padx=18, pady=10).pack(side=LEFT, padx=18)
Button(btn_frame, text="Delete", image=icon_delete, compound=LEFT, font=FONT, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=delete_data, bd=0, relief=RIDGE, padx=18, pady=10).pack(side=LEFT, padx=18)
Button(btn_frame, text="Export CSV", image=icon_csv, compound=LEFT, font=FONT, bg="#f39c12", fg=BTN_TEXT_COLOR, command=export_csv, bd=0, relief=RIDGE, padx=18, pady=10).pack(side=LEFT, padx=18)

window.mainloop()
