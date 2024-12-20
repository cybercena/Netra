from netra import *
import netra as netra


# Function to scan the network using ARP
def scan_network():
    local_ip = netra.get_local_ip()
    subnet = ".".join(local_ip.split('.')[:-1]) + ".0/24"
    devices = []
    

    # Create an ARP request packet
    arp_request = ARP(pdst=subnet)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether_frame / arp_request

    try:
        result = srp(packet, timeout=2, verbose=False)[0]
        for sent, received in result:
            hostname = resolve_hostname(received.psrc)
            devices.append((hostname, received.psrc, received.hwsrc))
    except PermissionError:
        messagebox.showerror("Error", "Run as Administrator for network scanning.")
    return devices, subnet

# Resolve hostname
def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

# Action for Option Buttons
def option_action(ip, mac):
    messagebox.showinfo("Option Action", f"Performing action on\nIP: {ip}\nMAC: {mac}")

# Start scan button action
def start_scan():
    # Hide table initially
    result_label.pack_forget()
    tree.pack_forget()
    table_frame.pack_forget()

    # Show progress bar
    result_text.set("Scanning Network...")
    progress_bar.pack(pady=5)
    progress_bar.start()

    # Start scanning in a new thread
    threading.Thread(target=scan_and_display).start()

# Function to scan and display results
def scan_and_display():
    global devices
    devices, subnet = scan_network()
    local_ip = netra.get_local_ip()
    public_ip = netra.get_public_ip()

    # Update Results Text
    result_text.set(f"Active devices: {len(devices)}\n"
                    f"Local IP: {local_ip}\n"
                    f"Public IP: {public_ip}\n"
                    f"Subnet: {subnet}")
    
    # Clear Previous Table Rows
    for row in tree.get_children():
        tree.delete(row)

    # Update Table with Data and Option Buttons
    for device in devices:
        tree.insert("", "end", values=(device[0], device[1], device[2]))

    # Hide progress bar and show table
    progress_bar.stop()
    progress_bar.pack_forget()
    result_label.pack(pady=10)
    table_frame.pack(pady=10)
    tree.pack()

#creating a function to exit the appplication
#creating a function to exit from the app 
def exit_app():
    root.quit()

#creating a function to save results
def save_scan_results(data_list):
    hide_all_frames()
    text_area = Text(save_scan_frame, wrap='word')
    text_area.pack(expand=True, fill='both')
    save_scan_frame.pack(fill = "both" , expand = 1)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"),
                                                        ("All files", "*.*")])
    
    if file_path:
        try:
            with open(file_path, 'w') as file:
                for item in data_list:
                    file.write(f"{item}\n")
        except Exception as e:
            messagebox.showerror("Save File", f"Failed to save file: {e}")


#creating a open file options  
def open_scan_results():
    hide_all_frames()
    open_scan_frame.pack(fill = "both" , expand = 1)
    #createa a text area for notepads
    # text_area = Text(open_scan_frame, wrap='word')
    # text_area.pack(expand=True, fill='both')

    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text files", "*.txt"),
                                                      ("All files", "*.*")])
    
    if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                data = []
                for line in lines:
                    ip, mac = line.strip().strip('()').split(',')
                    data.append((ip.strip("'"), mac.strip("'")))

                # Create and display the table
                columns = ("IP Address", "MAC Address")
                table = ttk.Treeview(open_scan_frame, columns=columns, show="headings")
                for col in columns:
                    table.heading(col, text=col)
                    table.column(col, anchor="center")

                for row in data:
                    table.insert("", "end", values=row)

                table.pack(fill="both", expand=1)

            except Exception as e:
                messagebox.showerror("Open File", f"Failed to open file: {e}")

 



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


# Progress Bar (Hidden initially)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")

# Result Output Label
result_text = tk.StringVar(value="")
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12))

# Table Frame
table_frame = tk.Frame(root)
tree = ttk.Treeview(table_frame, columns=("Hostname", "IP Address", "MAC Address", "Options"), show="headings")

# Table Columns
tree.heading("Hostname", text="Host Name")
tree.heading("IP Address", text="IP Address")
tree.heading("MAC Address", text="MAC Address")
tree.heading("Options", text="Options")

# Add Option Buttons for Each Row
def tree_insert_callback(event):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, 'values')
    option_action(values[1], values[2])

tree.bind("<Double-1>", tree_insert_callback)


# Pack the Table
tree.pack(side="left", fill="both", expand=True)

# Scrollbar for Table
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

#rescan button for the applicatioons
def on_enter(event):
    start_button.config(bg="#d4435c", fg="white")

def on_leave(event):
    start_button.config(bg="#4CAF50", fg="white")

start_button = Button(
    welcome_frame,
    text="Rescan",
    font=("Helvetica", 16, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    relief="flat",
    bd=0,
    command=scan_and_display # yesma start_app function lekhana parxa
)
start_button.pack(pady=30)

# Add hover effects
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

#creating a dummy functions
def dummy():
        pass

#creating a frames for different sections
#frame for new scan
new_scan_frame = Frame(root,width = width , height = height )
#frame for  open scan
open_scan_frame = Frame(root,width = width , height = height )
#frame for save scan result menu
save_scan_frame = Frame(root,width = width , height = height )

#frame for port scanning 
port_scan_frame = Frame(root,width = width , height=height )
#frame for documentation
documentation_frame = Frame(root, width = width , height = height)
#frame for about 
about_frame = Frame(root, width = width , height = height )

#creating a list of frames used in program
frame_list = [welcome_frame,save_scan_frame]

#functions to hide other frames and deleting widgets
def hide_all_frames():

    for frame in frame_list:
        frame.pack_forget()
        for widget in frame.winfo_children():
            widget.destroy()

#creating a function to create a navigation bar
def create_navbar():

    #creating a menu bar with options
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    #creating a menus in menubar
    file_menu = Menu(menu_bar, tearoff=0)
    tools_menu = Menu(menu_bar, tearoff=0)
    help_menu = Menu(menu_bar, tearoff=0)
    
    #creating a menu tab and menu options
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Scan", command=dummy)
    file_menu.add_command(label="Open Scan Results", command=open_scan_results)
    file_menu.add_command(label="Save Scan Results", command=save_scan_results)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)


    #creating a tools menu and menu options
    menu_bar.add_cascade(label="Astras", menu=tools_menu)
    tools_menu.add_command(label="IP lookup", command=dummy)
    tools_menu.add_command(label="Port Scanner", command=dummy)
    tools_menu.add_command(label="", command=dummy)
    tools_menu.add_separator()
    tools_menu.add_command(label="Exit", command=dummy)
    
    #creating a help menu and menus
    menu_bar.add_cascade(label="Help", menu = help_menu)


# Main App Interface
def build_main_app():
    main_app_frame.pack_forget()


    #callling function to show navigation bar
    create_navbar()
    #calling function to scan the network
    scan_and_display()


root.mainloop()
