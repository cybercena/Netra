from NetrasLib import *

# Create the root windows.
root = Tk()
root.title("Netra - Network Scanner")
root.geometry("600x600")
root.config(bg="#1e1e2e")
height = 600
width= 600

#creating functions for the functionalites
def start_app():
    welcome_frame.pack_forget()
    main_app_frame.pack(fill="both", expand=True)
    # create_menu()
    build_main_app()

#creating testy function
def testy():
    pass

# creating Welcome Page Frame
welcome_frame = Frame(root, bg="#1e1e2e")
welcome_frame.pack(fill="both", expand=True)

# creating logo for welcome page
logo_image = Image.open("logo1.ico")  # Replace with your logo file path
logo_image = logo_image.resize((313, 300))  # Resize if needed
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(welcome_frame, image=logo_photo, bg="#1e1e2e")
logo_label.pack(pady=50)  # Adjust padding


# adding title for welcome page
title_label = Label(
    welcome_frame,
    text="Welcome to Netra",
    font=("Helvetica", 24, "bold"),
    fg="#f8f8f2",
    bg="#1e1e2e"
)
title_label.pack()

# Adding qoute for the welcome page
quote_label = Label(
    welcome_frame,
    text = "\"The Third Eye of Security: Uncover, Analyze, Secure.\"",
    font=("Helvetica", 14, "italic"),
    fg="#bd93f9",
    bg="#1e1e2e",
    wraplength=500,
    justify="center"
)
quote_label.pack(pady=10)
#button with hover effects
def on_enter(event):
    start_button.config(bg="#d4435c", fg="white")

def on_leave(event):
    start_button.config(bg="#4CAF50", fg="white")

start_button = Button(
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
start_button.pack(pady=30)

# Add hover effects
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

# Main Application Frame
main_app_frame = Frame(root, bg="white")
# Function to transition to the main app


# Main App Interface
def build_main_app():

    #creating a dummy functions
    def dummy():
        pass

    #creating a menu bar with options
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    #creating a file menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Scan", command=new_scan)
    file_menu.add_command(label="Open Scan Results", command=dummy)
    file_menu.add_command(label="Save Scan Results", command=dummy)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)



root.mainloop()
