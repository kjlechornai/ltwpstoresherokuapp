from tkinter import *
from tkinter import messagebox
import requests
import json

# VARIABLES
url = 'http://localhost:8000/api/'

# FUNCTIONS
def retrieve_items():
    if token_out:
        headers = {
            'Authorization': f'Token {token_out}'
        }
        r = requests.get(url, headers=headers)
        out_data = json.loads(r.text)
        # print(out_data[0])
        data = []
        for out in out_data:
            res = out.values()
            data.append(list(res))
        items_listbox.insert(END, 'ITEM NAME         ' + 'QTY   ' + 'UNIT    ' + 'STATUS  ' + 'SHELF LOCATION')
        for k in data:
            items_listbox.insert(END, str(k))

def search_items():
    items_listbox.delete(0, END)
    qs = search_entry.get()
    if token_out:
        headers = {
            'Authorization': f'Token {token_out}'
        }
        req = requests.get(url + f'?name={qs}', headers=headers)
        data_out = json.loads(req.text)
        data = []
        for out in data_out:
            res = out.values()
            data.append(list(res))
        for k in data:
            items_listbox.insert(END, str(k))

def select_item():
    qs = search_entry.get()
    # search logic
    

def login():
    global token_out
    # username -> admin
    # password -> storesadmin
    username = username_entry.get()
    password = password_entry.get()
    if username == '' or password == '':
        messagebox.showerror('Required fields', 'username/password should not be empty')
    else:
        data = {
            'username':username,
            'password':password
        }
        try:
            response = requests.post(url+'api-auth-token', data=data)
            resp_dict = json.loads(response.text)
            token_out = resp_dict['token']
        except Exception as e:
            messagebox.showerror('login failure', 'login credentials invalid, please try again')
    # login message
    messagebox.showinfo('success', 'you are successfully logged in')
    # clear the entry boxes
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    search_entry.focus()
    
    retrieve_items()

def clear():   
    search_entry.delete(0, END)
    items_listbox.delete(0, END)


app = Tk()

# USERNAME
username_text = StringVar()
username_label = Label(app, text='username', fg='red', font='arial 8 bold')
username_entry = Entry(app, textvariable=username_text)
username_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
username_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

# PASSWORD
password_text = StringVar()
password_label = Label(app, text='password', fg='red', font='arial 8 bold')
password_entry = Entry(app, show='*',textvariable=password_text)
password_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
password_entry.grid(row=0, column=3, padx=10, pady=10, sticky=W)

# LOGIN
login_button = Button(app, text='login', fg='red', font='arial 8 bold', command=login)
login_button.grid(row=0, column=4, padx=10, pady=10, sticky=W)

# SEARCH
search_text = StringVar()
search_label = Label(app, text='search', font='arial 9 bold')
search_entry = Entry(app, textvariable=search_text)
search_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
search_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

# SEARCH BUTTON
search_button = Button(app, text='search', font='arial 9 bold', command=search_items)
search_button.grid(row=1, column=2, padx=10, pady=10, sticky=W)

# CLEAR
clear_button = Button(app, text='clear',  font='arial 8 bold', command=clear)
clear_button.grid(row=1, column=3, padx=10, pady=10, sticky=W)

# LISTBOX
items_listbox = Listbox(app, border=1, height=10)
items_listbox.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=W+E)

# SCROLLBAR
items_scrollbar = Scrollbar(app)
items_scrollbar.grid(row=2, column=4, rowspan=10, sticky='ns')

items_listbox.configure(yscrollcommand=items_scrollbar.set)
items_scrollbar.configure(command=items_listbox.yview)
items_listbox.bind('<<ListboxSelect>>', select_item)

app.title('STORES MANAGEMENT')
app.geometry('750x500+0+0')
app.mainloop()





