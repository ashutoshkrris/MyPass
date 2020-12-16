import string
import random
from tkinter import messagebox
from tkinter.constants import END
import tkinter as tk
import pyperclip
import pandas as pd


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    password = ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase +
                                     string.digits) for _ in range(12))
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- RETRIEVE PASSWORD ------------------------------- #

def retrieve_password():
    website_name = website_retrieve_entry.get()
    email = email_retrieve_entry.get()
    if len(website_name) == 0 or len(email) == 0:
        messagebox.showinfo(
            title="Error", message="Please make sure you haven't left any field empty.")
    else:
        df = pd.read_csv("password_file.csv")
        try:
            data = df.loc[(df["Website"] == website_name) & (
                df["Email/Username"] == email)].values[0]
            password = data[len(data)-1]
            password_retrieve_entry.configure(state='normal')
            password_retrieve_entry.insert(0, password)
            pyperclip.copy(password)
            password_retrieve_entry.configure(state='disabled')
        except IndexError:
            messagebox.showinfo(
                title="Error", message="Please make sure you have entered correct details.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_name = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website_name) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Error", message="Please make sure you haven't left any field empty.")
    else:
        is_ok = messagebox.askokcancel(
            title=website_name, message=f"These are the details entered : \n\nEmail: {email} \nPassword: {password} \n\nIs it OK to save?")

        if is_ok:
            pass_dict = {
                "Website": [website_name],
                "Email/Username": [email],
                "Password": [password]
            }
            df = pd.DataFrame.from_dict(pass_dict)
            df.to_csv("password_file.csv")

            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

EMAIL_FIELD = "email@example.com"

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(height=200, width=200)
logo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# ---------------------------- ADD PASSWORD ------------------------------- #

# Labels
add_label = tk.Label(text="Add Password", font=("Courier", 20, "bold"))
add_label.grid(row=1, column=1)

website_label = tk.Label(text="Website : ")
website_label.grid(row=2, column=0)

email_label = tk.Label(text="Email / Username : ")
email_label.grid(row=3, column=0)

password_label = tk.Label(text="Password : ")
password_label.grid(row=4, column=0)

# Entries
website_entry = tk.Entry(width=35)
website_entry.grid(row=2, column=1, columnspan=2)
website_entry.focus()

email_entry = tk.Entry(width=35)
email_entry.grid(row=3, column=1, pady=5, columnspan=2)
email_entry.insert(0, EMAIL_FIELD)

password_entry = tk.Entry(width=21)
password_entry.grid(row=4, column=1, columnspan=2)

# Buttons
generate_password = tk.Button(
    text="Generate Password", command=password_generator)
generate_password.grid(row=4, column=2)

add_button = tk.Button(text="Add Password", width=36, command=save)
add_button.grid(row=5, column=1, pady=5, columnspan=2)


# ---------------------------- RETRIEVE PASSWORD ------------------------------- #

or_label = tk.Label(text="OR", font=("Courier", 50, "bold"))
or_label.grid(row=8, column=1)

retrieve_label = tk.Label(text="Retrieve Password",
                          font=("Courier", 20, "bold"))
retrieve_label.grid(row=10, column=1)

website_retrieve_label = tk.Label(text="Website : ")
website_retrieve_label.grid(row=12, column=0)

email_retrieve_label = tk.Label(text="Email / Username : ")
email_retrieve_label.grid(row=13, column=0)

password_label = tk.Label(text="Password : ")
password_label.grid(row=14, column=0)

website_retrieve_entry = tk.Entry(width=35)
website_retrieve_entry.grid(row=12, column=1, columnspan=2)

email_retrieve_entry = tk.Entry(width=35)
email_retrieve_entry.grid(row=13, column=1, pady=5, columnspan=2)
email_retrieve_entry.insert(0, EMAIL_FIELD)

password_retrieve_entry = tk.Entry(width=35, state='disabled')
password_retrieve_entry.grid(row=14, column=1, columnspan=2)

retrieve_button = tk.Button(
    text="Retrieve Password", width=36, command=retrieve_password)
retrieve_button.grid(row=16, column=1, pady=5, columnspan=2)

copyright_label = tk.Label(text="Ashutosh Krishna\n 2020")
copyright_label.grid(row=20, column=1)

window.mainloop()
