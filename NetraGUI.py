from NetrasLib import *

# Create the root windows.
root = Tk()
root.title("Netra - Network Scanner")
root.geometry("600x600")
root.config(bg="#1e1e2e")
height = 600
width= 600


#this is the sections were we can create a funcitons that we will going to connect with the functions.

#function to get local ip of own device
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except OSError:
        ip = None
    finally:
        s.close()
    return ip
#function to get the mac address of own device
def get_mac_add():
    pass
#single function to get the local ip and mac address, we add stattic add due to some problems
def get_local_ip_and_mac():
    local_ip = get_local_ip()
    local_mac = "aa:bb:c1:3a:7e:b1"
    return local_ip, local_mac

#function to create and send ARP request
def arp_request(ip):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    reply_arp, _ = srp(arp_request, timeout=3, verbose=False)
    if reply_arp:
        for _, received in reply_arp:
            return received.psrc, received.hwsrc
    return None

#function to scan the network with subnet
def scan_network(subnet):
    active_devices = []
    local_ip, local_mac = get_local_ip_and_mac()
    active_devices.append((local_ip, local_mac))

    with ThreadPoolExecutor(max_workers=200) as executor:
        futures = {executor.submit(arp_request, str(ip)): ip for ip in ipaddress.IPv4Network(subnet).hosts()}
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    active_devices.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")
    return active_devices

#createing a variable for subnet
subnet_var = StringVar()
#creating a function for new scan
def new_scan():
    hide_all_frames()
    new_scan_frame.pack(fill="both", expand=1)
    subnet_label = Label(new_scan_frame , text = "Entet the Subnet[192.168.18.0/24]")
    subnet_label.pack()
    subnet = Entry(new_scan_frame,width= 20 , textvariable=subnet_var).pack()
    scan_btn = Button(new_scan_frame,text = "Scan",width = 18 , command=validation_and_scan).pack()

#ip subnet formating  using regex
def validate_ip_subnet(ip_subnet):
    # Regular expression for validating an IP address with subnet mask
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){2}[0-9]{1,3}\.0/(?:[0-9]|[1-2][0-9]|3[0-2])$")

    return pattern.match(ip_subnet)

#validating ip scan
def validation_and_scan():
    subnet = subnet_var.get()
    if validate_ip_subnet(subnet):
        scan()
    elif subnet == "":
        messagebox.showerror("Error","No IP were entered !")
    else:
        messagebox.showerror("Error","The IP address and subnet format is incorrect.")   

#binding enter key for event triggering
root.bind('<Return>', lambda event: validation_and_scan())

#creating a actual scan funtion and printing the data

def scan():
    hide_all_frames()
    new_scan_frame.pack(fill="both", expand=1)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    active_device = Label(new_scan_frame, 
                          text=f"Active devices on : {current_time}", 
                          height=3,
                          font=('Helvetica', 14),  # Change font to 'Helvetica' with size 14
                          fg='blue')
    active_device.pack(fill='x')

    columns = ("IP Address", "MAC Address")
    table = ttk.Treeview(new_scan_frame, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center")

    # Example data
    subnet = subnet_var.get()
    data = scan_network(subnet)


    # Insert data into the table
    for row in data:
        table.insert("", "end", values=row)

    table.pack(fill="both", expand=1)

    save_btn = Button(new_scan_frame , text = "Save" , command=lambda:save_scan_results(data))
    save_btn.pack()


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

def validate_target_ip(target):
    pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    return pattern.match(target)

# Function to validate and perform port scanning
def validation_and_port_scan():
    global scan_type_combobox, protocol_combobox, target_for_portscan
    
    scan_type_value = scan_type_combobox.get()
    protocol_type_value = protocol_combobox.get()
    target = target_for_portscan.get()

    if validate_target_ip(target):
        port_scan(scan_type_value, protocol_type_value, target)
    elif target == "":
        messagebox.showerror("Error", "No IP was entered!")
    else:
        messagebox.showerror("Error", "The IP address format is incorrect.")



#creating a function to exit from the app 
def exit_app():
    root.quit()

 # Creating variables for inputs
target_for_portscan = StringVar()
scan_type = StringVar()
protocol_type = StringVar()



# Function to transition to the main app
def start_app():
    welcome_frame.pack_forget()
    main_app_frame.pack(fill="both", expand=True)
    # create_menu()
    build_main_app()

# # Function for animating text
# def animate_text():
#     text = '''  Welcome to Netra
#     Discover Analyze Secure'''
#     label_text = ""
#     #function for animation of the text.
#     def update_text(i=0):
#         nonlocal label_text
#         if i < len(text):
#             label_text += text[i]
#             quote_label.config(text=label_text)
#             i += 1
#             root.after(100, update_text, i)  # Call update_text again after 100ms

#     update_text()

# # Welcome Page Frame
welcome_frame = Frame(root, bg="#1e1e2e")
welcome_frame.pack(fill="both", expand=True)

# Logo (Add your logo path here)
logo_image = Image.open("logo1.ico")  # Replace with your logo file path
logo_image = logo_image.resize((313, 300))  # Resize if needed
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(welcome_frame, image=logo_photo, bg="#1e1e2e")
logo_label.pack(pady=50)  # Adjust padding


# Add Title
title_label = Label(
    welcome_frame,
    text="Welcome to Netra",
    font=("Helvetica", 24, "bold"),
    fg="#f8f8f2",
    bg="#1e1e2e"
)
title_label.pack()

# Add Quote
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
# Stylish Start Button with Hover Effects
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
    command=start_app
)
start_button.pack(pady=30)

# Add hover effects
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

# Main Application Frame
main_app_frame = Frame(root, bg="white")

# Main App Interface
def build_main_app():
    #creating a menu bar with options
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    def dummy():
        pass
    # File Menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Scan", command=new_scan)
    file_menu.add_command(label="Open Scan Results", command=dummy)
    file_menu.add_command(label="Save Scan Results", command=dummy)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)

    #Tools menu
    tools_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Tools", menu=tools_menu)
    tools_menu.add_command(label="Port Scanning", command=dummy)
    tools_menu.add_command(label="Ip lookup", command=dummy)

    #creating menu for setting
    settings_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Preferences", command=dummy)
    settings_menu.add_command(label="Network Settings", command=dummy)
    settings_menu.add_command(label="Update", command=dummy)

#creating some frames
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

#creating a list of frames.
frame_list = [new_scan_frame,open_scan_frame,save_scan_frame,documentation_frame,about_frame,port_scan_frame]

# frame_list = [new_scan_frame,open_scan_frame]

#functions to hide other frames and deleting widgets
def hide_all_frames():

    for frame in frame_list:
        frame.pack_forget()
        for widget in frame.winfo_children():
            widget.destroy()
        
        # for widget in new_scan_frame.winfo_children():
        #     widget.destroy()
    
    # new_scan_frame.pack_forget()
    # open_scan_frame.pack_forget()
    # save_scan_frame.pack_forget()


    

    

# build_main_app()

# # Start the text animation
# animate_text()

# Run the app
root.mainloop()
