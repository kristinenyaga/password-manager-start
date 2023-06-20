import random
from tkinter import *
from tkinter import messagebox
import pyperclip
import json
FONT = ("Arial", 16, "normal")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(5, 7)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]

    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = ''.join(password_list)
    window.clipboard_append(password)

    # password = ""
    # for char in password_list:
    #   password += char
    password_text.insert(END, password)
    # print(f"Your password is: {password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_text.get()
    password = password_text.get()
    email = email_text.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="warning", message="fill in all fields")
    else:
        is_ok = messagebox.askokcancel(
            title=website, message=f"Do you wish to save this:\n{website} \n{email}\n{password}")
        if is_ok:
          # open the file
            try:
                with open('data.json', 'r') as f:
                    data = json.load(f)

              # json.dump(new_data,f,indent=4)
              # load the old data/read from the file
            except FileNotFoundError:
                with open('data.json', 'w') as f:
                    json.dump(new_data, f, indent=4)

            else:
              # update the old data
                data.update(new_data)

                with open('data.json', 'w') as f:
                    # dump the updated data
                    json.dump(data, f, indent=4)
                    print(data)
            finally:
                web_text.delete(0, 'end')
                password_text.delete(0, 'end')
#---------------------------------SEARCH FOR PASSWORD------------------------------#
def search():
    search_button.config(bg="blue")
    search_text = web_text.get()

    if len(search_text) >0:
        try:
            with open('data.json','r') as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(
                title="404", message="the file does not exist")
        else:
            try:
                searched_data = data[search_text]
            except KeyError:
                messagebox.showinfo(
                title="404", message=f"details for the {search_text} don't exist")
            else:
                email=searched_data["email"]
                password=searched_data["password"]
                messagebox.showinfo(title="lookup",message=f"EMAIL: {email} \nPASSWORD: {password}")
    else:
        messagebox.showwarning(title="warning", message="enter something")


#---------------------------------SEARCH FOR PASSWORD------------------------------#


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)
canvas = Canvas(width=300, height=300, highlightthickness=0)
myimg = PhotoImage(file='logo.png')
canvas.create_image(50, 50, image=myimg, anchor='nw')
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ", font=FONT, pady=10)
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username: ",
                    font=FONT, pady=10)
email_label.grid(row=2, column=0)

password_label = Label(text="Password: ", font=FONT, pady=10)
password_label.grid(row=3, column=0)


search_button = Button(text="search", width=17, height=2, command=search)
search_button.grid(column=2, row=1, columnspan=2)

web_text = Entry(width=30, font=FONT)
# Puts cursor in textbox.
web_text.focus()
# Adds some text to begin with.
# Get's current value in textbox at line 1, character 0
web_text.grid(row=1, column=1, columnspan=1)


email_text = Entry(width=45, font=FONT)
# Puts cursor in textbox.
email_text.focus()
# Adds some text to begin with.
email_text.insert(END, "nyagakristine@gmail.com")
# Get's current value in textbox at line 1, character 0
email_text.grid(row=2, column=1, columnspan=2)

password_text = Entry(width=30, font=FONT)
# Puts cursor in textbox.
password_text.focus()
# Adds some text to begin with.
# Get's current value in textbox at line 1, character 0
password_text.grid(row=3, column=1)

generate_pass_button = Button(
    text="Generate Password", height=2, command=generate_password)
generate_pass_button.grid(column=2, row=3)


add_button = Button(text="Add", width=62, height=2, command=save)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()
