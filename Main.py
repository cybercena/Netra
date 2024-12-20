#this is the final touch of the project netra
import netra as netra
from netra import *

# creating dummy function 
def dummy():
    pass

#creating a function to display random qoute as moto
def update_random_moto():
    random_moto = random.choice(quotes)
    moto.config(text = random_moto)
    root.after(2000,update_random_moto)

#creating hover effect for the start button of welcome page
def on_enter(event):
    app_start_button.config(bg="#d4435c", fg="white")

def on_leave(event):
    app_start_button.config(bg="#4CAF50", fg="white")

#creating a function to exit from the application
def exit_app():
    root.quit()


#creating a function to create a menubar with menus
def create_menubar():
    menu_bar = Menu(root)
    root.config(menu=menu_bar)
    #creating a menus in menubar
    #creating a file menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    #creating a sub menu in file menu
    file_menu.add_command(label="New scan", command=dummy)
    file_menu.add_command(label="Open scan", command=dummy)
    file_menu.add_command(label="Save scan", command=dummy)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)
    
def start_app():
    #creating a welcome page
    create_menubar()
    hide_all_frames()

#starting of GUI code
# Create the main window and initialize the value for height and width with title for the window 
root = Tk()
#getting the screen width and height
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
bg_color = "#1e1e2e"
root.title("NETRA - Network Scanner")
root.geometry(f"{screen_width}x{screen_height}")
root.config(bg= bg_color)

#creating a welcome page and welcome frame
welcome_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creatinng a frame for welcome page
network_scan_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for Network Scanning pages
scan_result_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for scan result page
about_frame = Frame(root, width = screen_width , height = screen_height, bg = bg_color)   #creating a frame for about page
port_scan_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for port scanning page
documentation_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for documentation page
#creating a list of frames used in the application
frame_list = [welcome_frame,network_scan_frame,scan_result_frame,about_frame,port_scan_frame,documentation_frame]

#creating a hide_all_frame functions to hide the other frame
def hide_all_frames():
    for frame in frame_list:
        frame.pack_forget()
        for widget in frame.winfo_children():
            widget.destroy()


#Creating a logo of netra for the welcome page
# creating logo for welcome page
welcome_frame.pack(fill="both", expand=True)
logo_image = Image.open("logo1.ico")  #selecting the image file that we want to show
logo_image = logo_image.resize((313, 300))  # the size can be resize if needed
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(welcome_frame, image=logo_photo, bg = bg_color)
logo_label.pack(pady=50)  # Adjust padding

#creating a welcome message for the welcome page
welcome_message = Label(welcome_frame, text="WELCOME TO NETRA", font=("Courier",
"25", "bold"), fg="white", bg=bg_color)
welcome_message.pack()

#writing a moto for the welcome page about netra
#creating a list of qoutes
quotes = [
    "Scan smarter, not harder.",
    "Unveiling the network's secrets.",
    "Network scanning made simple.",
    "Your digital reconnaissance starts here.",
    "Every port tells a story.",
    "Mapping the digital frontier.",
    "Empowering cybersecurity professionals.",
    "Explore networks, safely and efficiently.",
    "The first step to security is discovery.",
    "Netra: Your vision into the network."
]

moto = Label(welcome_frame, text="Network Scanner", font=("Courier", "20"),  
fg="white", bg=bg_color)
moto.pack(pady=20)

#calling random_moto function to display random qoutes..
update_random_moto()

#creating a app start button to move to another page

app_start_button = Button(
    welcome_frame,
    text="Start",
    font=("Helvetica", 16, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    relief="flat",
    bd=0,
    command=start_app # yesma start_app function lekhana parxa
)
app_start_button.pack(pady=30)

# Add hover effects
app_start_button.bind("<Enter>", on_enter)
app_start_button.bind("<Leave>", on_leave)

# Create "Developed by" label and position it at the bottom left
developed_by_label = tk.Label(welcome_frame, text="Developed by Cybercena", font=("Arial", 10), anchor="w",bg = bg_color , fg = "white")
developed_by_label.pack(side="left", padx=10, pady=10)


# Create version label and position it at the bottom right
version_label = tk.Label(welcome_frame, text="Version 1.0", font=("Arial", 10), anchor="e", bg = bg_color , fg = "white")
version_label.pack(side="right", padx=10, pady=10)




root.mainloop()