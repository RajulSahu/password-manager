from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)
    password = "".join(password_list)
    pass_entry.delete(0, END)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_data():
    website = website_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    data_dict = {
        website: {
            "E-mail": email,
            "Password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showwarning(title="Oops!", message="Please don't leave any of the fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \n Email/Username: {email} \n "
                                               f"Password: {password} \n Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)

            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(data_dict, file, indent=4)
            else:
                data.update(data_dict)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                pass_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showwarning(title="Oops!", message="Website field empty!")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            messagebox.showwarning(title="Error Retrieving Data!", message="No Data file Found!")
        else:
            if website in data:
                email = data[website]["E-mail"]
                password = data[website]["Password"]
                messagebox.showinfo(title="Credentials Retrieved!", message=f"{website} Login credentials: \n "
                                                                            f"Email/Username: {email} \n "
                                                                            f"Password: {password}")
            else:
                messagebox.showwarning(title="Error Retrieving Data!",
                                       message="No Details file Found!\n Please check the "
                                               "website name you typed\n Search is case "
                                               "sensitive!")


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

# Entry
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "sahur5426@gmail.com")
pass_entry = Entry(width=33)
pass_entry.grid(row=3, column=1)

# Buttons
generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(row=3, column=2)
add_button = Button(text="Add", width=44, command=add_data)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
