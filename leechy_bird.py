# Author: Foster C. Williams
# Email: fosterclarksonwilliams@gmail.com
#github: github.com/fosdos

#Leechy Bird alpha 1.0


import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from PIL import Image, ImageTk
import thread
import time
import tkMessageBox
from fosbot import bot
from control import twitter_timer

class Leechy_Bird(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self,*args,**kwargs)
    self.title("Leechy Bird Alpha 1.0")
    self.title_fong = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
    self.geometry("325x505")
    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0,weight=1)
    container.grid_columnconfigure(0,weight=1)

    self.frames = {}
    for F in (StartPage, helpPage, mainPage, runPage, mainHelp, contactPage, donatePage):
      page_name = F.__name__
      frame = F(parent=container, controller=self)
      self.frames[page_name] = frame
      frame.grid(row=0,column=0,sticky="nsew")

    self.show_frame("StartPage")
  def show_frame(self, page_name):
    frame = self.frames[page_name]
    frame.tkraise()
class StartPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    label = tk.Label(self, text="Welcome to Leechy Bird!")
    label.pack(side="top", fill="x", pady=10)
    load = Image.open("leechy_logo.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.place(x=35,y=355)


    consumer_key_label = tk.Label(self, text="Consumer Key",pady=2, font=("Helvetica", 20))
    self.consumer_key_entry = tk.Entry(self, width= 30)
    consumer_secret_label = tk.Label(self, text="Consumer Secret",pady=2, font=("Helvetica", 20))
    self.consumer_secret_entry = tk.Entry(self, width=30)
    access_key_label = tk.Label(self, text="Access Key",pady=2, font=("Helvetica", 20))
    self.access_key_entry = tk.Entry(self, width=30)
    access_secret_label = tk.Label(self, text="Access Secret",pady=2, font=("Helvetica", 20))
    self.access_secret_entry = tk.Entry(self, width=30)
    login_button = tk.Button(self, text="Login", command=lambda: self.login_test(parent, controller), pady=10, bd= 2, width=10)
    help_button = tk.Button(self, text="Help", command=lambda: self.help(parent, controller), pady=10)
    spacer_label = tk.Label(self,text="")

    consumer_key_label.pack()
    self.consumer_key_entry.pack()
    consumer_secret_label.pack()
    self.consumer_secret_entry.pack()
    access_key_label.pack()
    self.access_key_entry.pack()
    access_secret_label.pack()
    self.access_secret_entry.pack()
    spacer_label.pack()
    login_button.pack()
    help_button.pack()
  def login_test(self, parent, controller):
    print "Login Test"
    login = False
    consumer_key = self.consumer_key_entry.get().strip()
    consumer_secret = self.consumer_secret_entry.get().strip()
    access_key = self.access_key_entry.get().strip()
    access_secret = self.access_secret_entry.get().strip()
    try:
      controller.mybot = bot(consumer_key, consumer_secret, access_key,access_secret)
      print "failing before login test"
      login = controller.mybot.get_user_name()
    except:
      login=False

    if (login!=False):
      controller.show_frame("mainPage")
      controller.frames['mainPage'].space_label2['text'] = "Welcome, " + login + "!"
    else:
      print "Login Fail"
      tkMessageBox.showerror("Error", " Could Not Log In\nCheck The Help Page")
  def help(self, parent, controller):
    controller.show_frame("helpPage")
class mainPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.prey_list_made = False
    self.controller = controller
    self.space_label2 = tk.Label(self)
    self.space_label2.pack()
    victim_label = tk.Label(self, text="Enter Users you want to leech from\nSeperated by a comma(case sensitive, NO SPACES)\n E.g. Anti,PG_Esam\nFIRST GENERATION MIGHT TAKE A LONG TIME")
    victim_label.pack(side="top", fill="x", pady=10)

    load = Image.open("leechy_logo.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.place(x=35,y=330)

    self.victim_entry = tk.Entry(self, width= 30)
    self.victim_entry.pack()

    self.space_label1 = tk.Label(self)
    self.space_label1.pack()

    self.generate_prey_button = tk.Button(self, text="Generate Prey List", height = 1, width = 20, command=lambda: self.gen_prey(parent, controller))
    self.generate_prey_button.pack()
    self.show_prey_button = tk.Button(self, text="Show Prey List", height = 1, width = 20, command=lambda: self.show_prey(parent, controller), state='disabled')
    self.show_prey_button.pack()
    self.start_button = tk.Button(self, text="Start!", height=1, width = 20, command=lambda: self.start(parent, controller), state='disabled')
    self.start_button.pack()

    self.space_label = tk.Label(self)
    self.space_label.pack()

    self.main_help_button= tk.Button(self, text="FAQ", height=1, width = 12, command=lambda: controller.show_frame('mainHelp'))
    self.main_help_button.pack()
    self.donate_button = tk.Button(self, text="Donate", height=1, width = 12, command=lambda: controller.show_frame('donatePage'))
    self.donate_button.pack()
    self.contact_button = tk.Button(self, text="Contact Me", height=1, width = 12, command=lambda: controller.show_frame('contactPage'))
    self.contact_button.pack()

    self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame('StartPage'))
    self.back_button.pack(side='bottom')
  def gen_prey(self, parent, controller):
    name_list = self.victim_entry.get().encode('ascii','ignore').strip(' ').split(',')
    print name_list
    try:
      controller.mybot.gen_follow_lists()
      controller.follow_list = controller.mybot.generate_long_leech_list(name_list)
      self.main_help_button['state'] = 'normal'
      self.donate_button['state'] = 'normal'
      self.contact_button['state'] = 'normal'
      self.generate_prey_button['state'] = 'normal'

      print controller.follow_list
      self.show_prey_button['state'] = 'normal'
      self.start_button['state'] = 'normal'
      self.space_label2['text'] = "List Generated, Ready to Start"
    except:
      tkMessageBox.showerror("Error", "Error generating list.\nPlease restart Leechy Bird ")
  def show_prey(self, parent, controller):
    prey_list = controller.follow_list
    display = "FOLLOW LIST:\n"
    for x in range(len(prey_list)):
      display = display + str(prey_list[x]) + ", "
      if ((x+10)%10==0):
        display = display + "\n"
    tkMessageBox.showinfo("Follow List", display)

  def start(self, parent, controller):
    self.controller.show_frame('runPage')
    print "sleeping for 5 seconds before starting..."
    time.sleep(5)
    print "Alright its time to gooooo"
    try:
      controller.mybot.start()
    except:
      self.controller.show_frame('mainPage')
      tkMessageBox.showerror("Error", "Something went wrong, please restart leechy bird")
      controller.destroy()



class runPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.space_label1 = tk.Label(self)
    self.space_label1.pack()
    self.space_label1 = tk.Label(self)
    self.space_label1.pack()
    self.space_label1 = tk.Label(self)
    self.space_label1.pack()
    self.running_label = tk.Label(self, text="Running Bot, check back later!")
    self.running_label.pack()
    button = tk.Button(self, text="Stop", command=lambda: self.controller.show_frame("mainPage"))
    button.pack()
    load = Image.open("leechy_logo.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.place(x=35,y=350)
class helpPage(tk.Frame):

    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      label = tk.Label(self, text="")
      label.pack(side="top", fill="x", pady=10)
      label1 = tk.Label(self, text="To get your keys follow this guide:")
      label1.pack()
      link = tk.Text(self, height = 5, font =("Helvetica", 10))
      link.insert('insert', "https://auth0.com/docs/connections/social/twitter\n\nNote: You can create an empty github repository for the website")
      link['state'] = 'disabled'
      link.pack()
      button = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
      button.pack(side='bottom')
      load = Image.open("contact_smol.png")
      render = ImageTk.PhotoImage(load)
      img = tk.Label(self, image=render)
      img.image = render
      img.place(x=35,y=175)
class mainHelp(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    label = tk.Label(self, text="FAQ")
    label.pack()
    load = Image.open("faq.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.place(x=15,y=0)
    button = tk.Button(self, text="Back", command=lambda: controller.show_frame("mainPage"))
    button.pack(side='bottom')
class contactPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    load = Image.open("contact.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.place(x=20,y=20)
    button = tk.Button(self, text="Back", command=lambda: controller.show_frame("mainPage"))
    button.pack(side='bottom')
class donatePage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    load = Image.open("donation.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.place(x=30,y=0)
    label = tk.Label(self, text="Donations are greatly appreciated!")
    label.pack()
    button = tk.Button(self, text="Back", command=lambda: controller.show_frame("mainPage"))
    button.pack(side = 'bottom')
app = Leechy_Bird()
app.mainloop()
