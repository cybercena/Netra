from tkinter import *
from tkinter import Menu, messagebox ,ttk , filedialog
from scapy.all import ARP, Ether, srp
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import re
from datetime import datetime


# Create the main window and initialize the value for height and width with title for the window 
root = Tk()
height = 600
width= 600
root.title("NETRA")
root.geometry("600x600")


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

 


#creating a function to exit from the app 
def exit_app():
    root.quit()
#working on the port scanner 
 # Creating variables for inputs
target_for_portscan = StringVar()
scan_type = StringVar()
protocol_type = StringVar()

# Creating the port scanning UI
def port_scanner():
    hide_all_frames()
    port_scan_frame.pack(fill="both", expand=1)

    # Target IP Label and Entry
    target_ip_label = Label(port_scan_frame, text="Target IP:")
    target_ip_label.grid(row=1, column=0)
    global target_ip_entry
    target_ip_entry = Entry(port_scan_frame, width=18, textvariable=target_for_portscan)
    target_ip_entry.grid(row=1, column=1)

    # Scan Type Drop-down Menu
    scan_type_label = Label(port_scan_frame, text="Scan Type:")
    scan_type_label.grid(row=2, column=0)
    global scan_type_combobox
    scan_type_combobox = ttk.Combobox(port_scan_frame, values=["Single Port", "Multiple Ports", "Range of Ports"], state='readonly')
    scan_type_combobox.set("Single Port")
    scan_type_combobox.grid(row=2, column=1, padx=5, pady=5)

    # Port Label and Entry Box
    port_input_label = Label(port_scan_frame, text="Port(s):")
    port_input_label.grid(row=3, column=0)
    global port_input_box
    port_input_box = Entry(port_scan_frame, width=24)
    port_input_box.grid(row=3, column=1)

    # Protocol Drop-down Menu
    protocol_label = Label(port_scan_frame, text="Protocol:")
    protocol_label.grid(row=4, column=0, padx=5, pady=5)
    global protocol_combobox
    protocol_combobox = ttk.Combobox(port_scan_frame, values=["TCP", "UDP", "SYN"], state='readonly')
    protocol_combobox.set("TCP")
    protocol_combobox.grid(row=4, column=1, padx=5, pady=5)

    # Scan Button
    port_scan_button = Button(port_scan_frame, text="Start Scan", command=validation_and_port_scan)
    port_scan_button.grid(row=5, column=1)

# Function to validate the IP address
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

# Function to perform port scanning (dummy implementation)
def port_scan(scan_type, protocol_type, target):
    if scan_type == "Single Port":
        print(f"Single Port Scan on {target} using {protocol_type} protocol")
    elif scan_type == "Multiple Ports":
        print(f"Multiple Ports Scan on {target} using {protocol_type} protocol")
    elif scan_type == "Range of Ports":
        print(f"Range of Ports Scan on {target} using {protocol_type} protocol")
    else:
        print("Unknown scan type")




# def quick_scan():
#     clear_screen()
#creating dummy funtions for menus
def intense_scan():
    messagebox.showinfo("Intense Scan", "Performing an intense scan...")

def ping_scan():
    messagebox.showinfo("Ping Scan", "Performing a ping scan...")


def udp_scan():
    messagebox.showinfo("UDP Scan", "Performing a UDP scan...")

def syn_scan():
    messagebox.showinfo("SYN Scan", "Performing a SYN scan...")

def custom_scan():
    messagebox.showinfo("Custom Scan", "Configuring a custom scan...")

def stop_scan():
    messagebox.showinfo("Stop Scan", "Stopping the scan...")

def ip_lookup():
    messagebox.showinfo("IP Lookup", "Looking up IP address...")


    

def ping():
    messagebox.showinfo("Ping", "Pinging IP address...")

def traceroute():
    messagebox.showinfo("Traceroute", "Performing traceroute...")

def service_version_detection():
    messagebox.showinfo("Service Version Detection", "Detecting service versions...")

def os_detection():
    messagebox.showinfo("OS Detection", "Detecting OS...")

def vulnerability_scanning():
    messagebox.showinfo("Vulnerability Scanning", "Scanning for vulnerabilities...")

def network_inventory():
    messagebox.showinfo("Network Inventory", "Creating network inventory...")

def scripting_engine():
    messagebox.showinfo("Scripting Engine", "Using Nmap Scripting Engine (NSE)...")

def firewall_evasion():
    messagebox.showinfo("Firewall Evasion", "Applying firewall evasion techniques...")

def preferences():
    messagebox.showinfo("Preferences", "Opening preferences...")

def network_settings():
    messagebox.showinfo("Network Settings", "Configuring network settings...")

def update():
    messagebox.showinfo("Update", "Checking for updates...")

def documentation():
    hide_all_frames()
    documentation_frame.pack(fill="both",expand=1)

    text_widget = Text(documentation_frame,wrap = WORD , height= 10 , width=50)
    text_widget.pack(fill = BOTH , expand = 1)

    #read the text from documentation file
    try:
        with open("documentation.txt","r") as file:
            documentation_text = file.read()
    except FileNotFoundError:
        messagebox.showerror("No Documentation")
    text_widget.insert(END,documentation_text)
    text_widget.config(state = DISABLED)
#function for the about function
def about():
    hide_all_frames()
    about_frame.pack(fill="both",expand=1)

    text_widget = Text(about_frame,wrap = WORD , height= 10 , width=50)
    text_widget.pack(fill = BOTH , expand = 1)

    #read the text from README.md file
    try:
        with open("README.md","r") as file:
            about_me = file.read()
    except FileNotFoundError:
        messagebox.showerror("No Documentation")
    text_widget.insert(END,about_me)
    text_widget.config(state = DISABLED)

def support():
    messagebox.showinfo("Support", "Contacting support...")




# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Scan", command=new_scan)
file_menu.add_command(label="Open Scan Results", command=open_scan_results)
# file_menu.add_command(label="Save Scan Results", command=save_scan_results)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

#Tools menu
tools_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tools", menu=tools_menu)
tools_menu.add_command(label="Port Scanning", command=port_scanner)
tools_menu.add_command(label="Ip lookup", command=documentation)




# # Scan Menu
# scan_menu = Menu(menu_bar, tearoff=0)
# menu_bar.add_cascade(label="Scan", menu=scan_menu)
# scan_menu.add_command(label="Quick Scan", command=quick_scan)
# scan_menu.add_command(label="Intense Scan", command=intense_scan)
# scan_menu.add_command(label="Ping Scan", command=ping_scan)
# scan_menu.add_command(label="Port Scan", command=port_scan)
# scan_menu.add_command(label="UDP Scan", command=udp_scan)
# scan_menu.add_command(label="SYN Scan", command=syn_scan)
# scan_menu.add_command(label="Custom Scan", command=custom_scan)
# scan_menu.add_command(label="Stop Scan", command=stop_scan)

# View Menu
# view_menu = Menu(menu_bar, tearoff=0)
# menu_bar.add_cascade(label="View", menu=view_menu)
# view_menu.add_command(label="Scan Results")
# view_menu.add_command(label="Network Map")
# view_menu.add_command(label="Logs")

# # Tools Menu
# tools_menu = Menu(menu_bar, tearoff=0)
# menu_bar.add_cascade(label="Tools", menu=tools_menu)
# tools_menu.add_command(label="IP Lookup", command=ip_lookup)
# tools_menu.add_command(label="Port Scanner", command=port_scanner)
# tools_menu.add_command(label="Ping", command=ping)
# tools_menu.add_command(label="Traceroute", command=traceroute)
# tools_menu.add_command(label="Service Version Detection", command=service_version_detection)
# tools_menu.add_command(label="OS Detection", command=os_detection)
# tools_menu.add_command(label="Vulnerability Scanning", command=vulnerability_scanning)
# tools_menu.add_command(label="Network Inventory", command=network_inventory)
# tools_menu.add_command(label="Scripting Engine", command=scripting_engine)
# tools_menu.add_command(label="Firewall Evasion", command=firewall_evasion)

# Settings Menu
settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Preferences", command=preferences)
settings_menu.add_command(label="Network Settings", command=network_settings)
settings_menu.add_command(label="Update", command=update)

# Help Menu
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Documentation", command=documentation)
help_menu.add_command(label="About", command=about)
help_menu.add_command(label="Support", command=support)

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



#creating mainloop for window existing.
root.mainloop()
