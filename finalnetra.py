import netra as netra
from netra import *
from reportlab.lib import colors
from tkinter.messagebox import showerror, showinfo
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
# creating dummy function 
def dummy():
    print("button clicked")

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

def generate_pdf_from_txt(tool_name, network_range, total_ips_scanned):
    try:
        # Select the .txt file containing the data
        root = Tk()
        root.withdraw()  # Hide the root window
        txt_file_path = askopenfilename(filetypes=[("Text Files", "*.txt")], title="Select TXT File")
        
        if not txt_file_path:
            print("File selection canceled.")
            return

        # Read data from the selected file
        with open(txt_file_path, 'r') as file:
            lines = file.readlines()
        data = []
        for line in lines:
            ip, mac = line.strip().strip("()").split(", ")
            data.append((ip.strip("'"), mac.strip("'"), "Active"))

        # Ask where to save the PDF file
        pdf_file_path = asksaveasfilename(defaultextension=".pdf", 
                                          filetypes=[("PDF Files", "*.pdf")], 
                                          title="Save Report As")
        if not pdf_file_path:
            print("PDF generation canceled.")
            return

        # Create the PDF document
        pdf = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        styles = getSampleStyleSheet()

        # Header Section
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = Paragraph("<b>Host Discovery Report</b>", styles["Title"])
        overview_title = Paragraph("<b>1. Overview</b>", styles["Heading2"])
        overview = Paragraph(f"""
        <b>Tool Used</b>: {tool_name}<br/>
        <b>Report Generated On</b>: {timestamp}<br/>
        <b>Network Range</b>: {network_range}<br/>
        <b>Total IPs Scanned</b>: {total_ips_scanned}<br/>
        <b>Active Hosts Detected</b>: {len(data)}<br/>
        """, styles["BodyText"])

        spacer = Spacer(1, 12)

        # Host Discovery Details Section
        discovery_title = Paragraph("<b>2. Host Discovery Details</b>", styles["Heading2"])
        discovery_details = Paragraph(f"""
        The host discovery scan was conducted using {tool_name} to identify active devices within the network range {network_range}. 
        The scan detected {len(data)} active hosts out of {total_ips_scanned} total IP addresses. Each detected device's IP and MAC address were recorded, 
        providing a snapshot of the network's current state.
        """, styles["BodyText"])

        spacer_after_details = Spacer(1, 12)

        # Detected Hosts Table
        table_title = Paragraph("<b>3. Detected Hosts</b>", styles["Heading2"])
        table_data = [["S.No", "IP Address", "MAC Address", "Status"]]  # Table header
        for i, (ip, mac, status) in enumerate(data, start=1):
            table_data.append([i, ip, mac, status])

        # Create the table
        table = Table(table_data)
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ])
        )

        # Watermark Function
        def add_watermark(canvas, doc):
            canvas.saveState()

            # Set image position and size
            image_path = "/home/cybercena/Desktop/CyberAstras/Netra/logo1.ico"  # Specify the path to your image
            x_position = 20  # X position of the image
            y_position = 680  # Y position of the image
            width = 100  # Width of the image
            height = 100  # Height of the image
            transparency = 0.2  # Set transparency level (0 is fully transparent, 1 is fully opaque)
            canvas.setFillAlpha(transparency)
            # Draw the image on the PDF (you can change the position and size as needed)
            canvas.drawImage(image_path, x_position, y_position, width=width, height=height, mask='auto')

            canvas.restoreState()

        # Assign the watermark callback
        pdf.onFirstPage = add_watermark

        # Build the PDF
        elements = [
            title,
            spacer,
            overview_title,
            overview,
            spacer,
            discovery_title,
            discovery_details,
            spacer_after_details,
            table_title,
            table,
        ]
        pdf.build(elements)
        showinfo("Success", f"PDF report generated successfully: {pdf_file_path}")
    except Exception as e:
        showerror("Error", f"An error occurred: {e}")


#creating a function to save results
def save_scan_results(data_list):
    # network_scan_frame.pack_forget()
    # text_area = Text(scan_results_frame, wrap='word')
    # text_area.pack(expand=True, fill='both')
    network_scan_frame.pack(fill = "both" , expand = 1)
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
    # Update the scan button to allow rescanning
    scan_button.config(text="Scan", command=show_scan_results)
    
    

    # Prompt the user to select a file
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text files", "*.txt"),
                                                      ("All files", "*.*")])
    if file_path:
        try:
            # Read and process the file data
            with open(file_path, 'r') as file:
                lines = file.readlines()

            data = []
            for line in lines:
                # Clean and parse the line
                line = line.strip().strip('()')  # Remove parentheses
                ip, mac = line.split(',')        # Split into IP and MAC
                ip = ip.strip().strip("'")       # Remove quotes from IP
                mac = mac.strip().strip("'")     # Remove quotes from MAC
                data.append((ip, mac))           # Append cleaned data
            # Clear previous contents in the frame
            # scan_results_frame.pack_forget()
            for widget in scan_results_frame.winfo_children():
                widget.pack_forget()
            scan_results_frame.pack()
            # Create and display the table
            columns = ("IP Address", "MAC Address")
            table = ttk.Treeview(scan_results_frame, columns=columns, show="headings")
            table.pack(fill="both", expand=1, padx=10, pady=10)

            # Configure column headers
            for col in columns:
                table.heading(col, text=col)
                table.column(col, anchor="center", width=150)
            

            # Insert the cleaned data into the table
            for row in data:
                table.insert("", "end", values=row)

        except Exception as e:
            # Show an error message if something goes wrong
            messagebox.showerror("Open File", f"Failed to open file: {e}")

 


#creating a function to create a menubar with menus
def create_menubar():
    menu_bar = Menu(root)
    root.config(menu=menu_bar)
    #creating a menus in menubar
    #creating a file menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    #creating a sub menu in file menu
    file_menu.add_command(label="New scan", command=start_app)
    file_menu.add_command(label="Open scan", command=open_scan_results)
    file_menu.add_command(label="Save scan", command=dummy)
    tool_name = "Netra"
    network_range = ip_to_cidr(local_ip)
    total_ips_scanned = 256
    file_menu.add_command(label="Generate Report",command=lambda:generate_pdf_from_txt(tool_name, network_range, total_ips_scanned))

    file_menu.add_command(label="Exit", command=exit_app)

    #creating a Astras menu 
    astras_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Astras", menu=astras_menu)
    #creating a sub menu in astras menu
    astras_menu.add_command(label="Port Scanner", command=open_tools_window)
    astras_menu.add_command(label="IP lookup", command=open_ip_lookup_window)
    astras_menu.add_command(label="Ping",command=dummy)
    astras_menu.add_command(label="Traceroute",command=dummy)

    #creating a help menu

    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    #creating a sub menu in help menu
    help_menu.add_command(label="About", command=dummy)
    help_menu.add_command(label="Contact us", command=dummy)
    help_menu.add_command(label="FAQ", command=dummy)
    help_menu.add_command(label="Report a bug", command=dummy)
    help_menu.add_command(label="License", command=dummy)
    help_menu.add_command(label="Terms of use", command=dummy)


#starting of GUI code
# Create the main window and initialize the value for height and width with title for the window 
root = Tk()
#getting the screen width and height
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
bg_color = "#1e1e2e"
font_color = "#ffffff"
root.title("NETRA - Network Scanner")
root.geometry(f"{screen_width}x{screen_height}")
root.config(bg= bg_color)

#creating a welcome page and welcome frame
welcome_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creatinng a frame for welcome page
welcome_frame.pack()
network_scan_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for Network Scanning pages
scan_result_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for scan result page
about_frame = Frame(root, width = screen_width , height = screen_height, bg = bg_color)   #creating a frame for about page
port_scan_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for port scanning page
documentation_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for documentation page
progress_bar_frame = Frame(root, width = screen_width, height = screen_height, bg = bg_color)   #creating a frame for progress bar page
detail_section = Frame(network_scan_frame, bg = bg_color)
scan_section = Frame(network_scan_frame, bg=bg_color)
open_scan_frame = Frame(root,width = screen_width , height = screen_height )
#frame for save scan result menu
save_scan_frame = Frame(root,width = screen_width , height = screen_height )
#creating a list of frames used in the application
frame_list = [welcome_frame,network_scan_frame,scan_result_frame,about_frame,port_scan_frame,documentation_frame,progress_bar_frame,detail_section,scan_section,open_scan_frame,save_scan_frame]

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

# Create "Developed by" label and position it at the bottom left
developed_by_label = Label(welcome_frame, text="Developed by Cybercena", font=("Arial", 10), anchor="w",bg = bg_color , fg = "white")
developed_by_label.pack(side="left", padx=10, pady=10)

# Create version label and position it at the bottom right
version_label = Label(welcome_frame, text="Version 1.0", font=("Arial", 10), anchor="e", bg = bg_color , fg = "white")
version_label.pack(side="right", padx=10, pady=10)
test_label = Label(network_scan_frame, text = "testing hai !", font=("Arial", 10), anchor="e", bg = bg_color ,
fg = "white")
#creating a app start function
def start_app():
    #creating a welcome page
    create_menubar()
    welcome_frame.forget()
    network_scan_frame.pack(fill = "both" , expand = 1)
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
    command= start_app # yesma start_app function lekhana parxa
)
app_start_button.pack(pady=30)

# creating logo for welcome page
welcome_frame.pack(fill="both", expand=True)
network_info_frame = Frame(network_scan_frame , bg=bg_color)
network_info_frame.pack(fill="both", expand=True)

# Function to get network information
def get_network_info():
    # Get the local IP address
    local_ip = socket.gethostbyname(socket.gethostname())
    
    # Get the public IP address by using an external service
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except requests.RequestException:
        public_ip = "Unavailable"

    # Get the subnet mask
    subnet_mask = None
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # Look for IPv4 address
                # Check if it's a non-loopback interface and matches the local IP
                if local_ip.startswith(addr.address[:local_ip.rfind('.')]):
                    subnet_mask = addr.netmask
                    break
        if subnet_mask:
            break

    return local_ip, public_ip, subnet_mask


# Example usage:
local_ip, public_ip, subnet_mask = get_network_info()
#creating a function to create a cidr notation
def ip_to_cidr(local_ip):
    # Convert IP to network
    network = ipaddress.IPv4Network(local_ip + '/24', strict=False)  # Using a /24 subnet for simplicity
    return f"{network.network_address}/24"

subnet = ip_to_cidr(local_ip)

#local ip label
local_ip_label = Label(network_info_frame, text=(f"Local IP:{local_ip}"), font=("Arial", 12), bg=bg_color, fg=font_color)
local_ip_label.pack(anchor="w", padx=10, pady=5)

# Public IP label
public_ip_label = Label(network_info_frame, text=(f"Public IP: {public_ip}"), font=("Arial", 12), bg=bg_color, fg=font_color)
public_ip_label.pack(anchor="w", padx=10, pady=5)

# Subnet label
subnet_label = Label(network_info_frame, text=(f"Subnet: {subnet_mask}"), font=("Arial", 12), bg=bg_color, fg=font_color)
subnet_label.pack(anchor="w", padx=10, pady=5)

# Scan button
scan_button = Button(network_info_frame, text="Start Scan", bg=bg_color, fg=font_color, font=("Arial", 12), command=lambda: show_scan_results())
scan_button.pack(pady=10)


# Section 2: Scan Results Section (Initially Hidden)
scan_results_frame = Frame(network_scan_frame, bg=bg_color)


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
    local_ip, public_ip, _ = get_network_info()
    local_mac = "94:65:9c:58:b2:45"
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


def scan():
    scan_results_frame.pack(fill="both", expand=1)
    scan_button.config(text="Rescan", command=show_scan_results)
    # Clear previous scan results (if any)
    for widget in scan_results_frame.winfo_children():
        widget.pack_forget()
        
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    active_device = Label(scan_results_frame, 
                          text=f"Active devices on : {current_time}", 
                          height=3,
                          font=('Helvetica', 14),  # Change font to 'Helvetica' with size 14
                          fg='blue')
    active_device.pack(fill='x')

    columns = ("IP Address", "MAC Address")
    table = ttk.Treeview(scan_results_frame, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center")

    data = scan_network(subnet)

    # Insert data into the table
    for row in data:
        table.insert("", "end", values=row)

    # table.pack(fill="both", expand=1)
    table.pack(fill="both", expand=1, pady=(0, 50))  # Move the table up by reducing bottom padding


    save_btn = Button(scan_results_frame , text = "Save" , command=lambda:save_scan_results(data))
    save_btn.pack()


# Function to show scan results and reveal the second section
def show_scan_results():
    # Show the second section (scan results)
    scan_button.config(text="Rescan", command=show_scan_results)
    scan_results_frame.pack(fill="both", expand=True, pady=20)
    scan()
    

#creating a ui and function for port scanner
 # Creating variables for inputs

# Initialize Colorama
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

# Initialize global variables
tool_window = None
ip_lookup_window = None
target_for_portscan = StringVar()

def is_port_open(host, port):
    """
    Determine whether `host` has the `port` open.
    """
    # Create a new socket
    s = socket.socket()
    try:
        # Try to connect to host using that port
        s.connect((host, port))
        s.settimeout(0.2)
    except:
        # Cannot connect, port is closed
        return False
    else:
        # Connection established, port is open!
        return True

def parse_port_range(port_input):
    """
    Parse port input to determine if it's a single port or a range.
    """
    if '-' in port_input:
        start_port, end_port = map(int, port_input.split('-'))
        return range(start_port, end_port + 1)
    else:
        port = int(port_input)
        return [port]

def validation_and_port_scan():
    """
    Validate inputs and perform port scan.
    """
    host = target_ip_entry.get().strip()
    port_input = port_input_box.get().strip()
    protocol = protocol_combobox.get()
    result_text.delete("1.0", END)

    # Validate host and port input
    if not host:
        result_text.insert(END, "Error: Please enter a valid Target IP.\n", "error")
        return
    if not port_input:
        result_text.insert(END, "Error: Please enter a valid Port or Range.\n", "error")
        return

    try:
        ports = parse_port_range(port_input)
    except ValueError:
        result_text.insert(END, "Error: Invalid Port format.\n", "error")
        return

    # Perform the port scan
    result_text.insert(END, f"Scanning {host} with protocol {protocol}...\n\n", "info")
    for port in ports:
        if is_port_open(host, port):
            result_text.insert(END, f"[+] {host}:{port} is open\n", "open")
        else:
            result_text.insert(END, f"[!] {host}:{port} is closed\n", "closed")

# Function to create the tools window
def open_tools_window():
    global tool_window
    if tool_window is None or not Toplevel.winfo_exists(tool_window):
        tool_window = Toplevel(root)
        tool_window.title("Tools")
        tool_window.geometry("500x500")
        tool_window.resizable(False, False)
        tool_window.config(bg=bg_color)


        # Target IP Label and Entry
        target_ip_label = Label(tool_window, text="Target IP:", bg=bg_color, fg=font_color)
        target_ip_label.grid(row=1, column=0, padx=5, pady=5)
        global target_ip_entry
        target_ip_entry = Entry(tool_window, width=25, textvariable=target_for_portscan)
        target_ip_entry.grid(row=1, column=1, padx=5, pady=5)

        # Scan Type Drop-down Menu
        scan_type_label = Label(tool_window, text="Scan Type:", bg=bg_color, fg=font_color)
        scan_type_label.grid(row=2, column=0, padx=5, pady=5)
        global scan_type_combobox
        scan_type_combobox = ttk.Combobox(tool_window, values=["Single Port", "Multiple Ports", "Range of Ports"], state='readonly')
        scan_type_combobox.set("Single Port")
        scan_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Port Label and Entry Box
        port_input_label = Label(tool_window, text="Port(s):", bg=bg_color, fg=font_color)
        port_input_label.grid(row=3, column=0, padx=5, pady=5)
        global port_input_box
        port_input_box = Entry(tool_window, width=25)
        port_input_box.grid(row=3, column=1, padx=5, pady=5)

        # Protocol Drop-down Menu
        protocol_label = Label(tool_window, text="Protocol:", bg=bg_color, fg=font_color)
        protocol_label.grid(row=4, column=0, padx=5, pady=5)
        global protocol_combobox
        protocol_combobox = ttk.Combobox(tool_window, values=["TCP", "UDP", "SYN"], state='readonly')
        protocol_combobox.set("TCP")
        protocol_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Scan Button
        port_scan_button = Button(tool_window, text="Start Scan", command=validation_and_port_scan, bg=bg_color, fg=font_color)
        port_scan_button.grid(row=5, column=1, padx=5, pady=5)

        # Result Display Text Box
        global result_text
        result_text = Text(tool_window, height=15, width=50, bg="black", fg="white", wrap=WORD)
        result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Add custom tags for result text
        result_text.tag_config("error", foreground="red")
        result_text.tag_config("open", foreground="green")
        result_text.tag_config("closed", foreground="gray")
        result_text.tag_config("info", foreground="blue")

    else:
        tool_window.lift()


def ip_lookup():
    ip_address = ip_entry.get().strip()
    if not ip_address:
        messagebox.showerror("Error", "Please enter a valid IP address.")
        return

    try:
        # Fetch IP information using ipinfo.io
        response = requests.get(f"http://ipinfo.io/{ip_address}/json")
        response.raise_for_status()
        ip_data = response.json()

        # Clear the result box
        result_text.delete(1.0, END)

        # Display the IP information
        if "error" in ip_data:
            result_text.insert(END, f"Error: {ip_data['error']['message']}\n", "error")
        else:
            result_text.insert(END, f"IP Address: {ip_data.get('ip', 'N/A')}\n", "info")
            result_text.insert(END, f"City: {ip_data.get('city', 'N/A')}\n", "info")
            result_text.insert(END, f"Region: {ip_data.get('region', 'N/A')}\n", "info")
            result_text.insert(END, f"Country: {ip_data.get('country', 'N/A')}\n", "info")
            result_text.insert(END, f"Organization: {ip_data.get('org', 'N/A')}\n", "info")
            result_text.insert(END, f"Location: {ip_data.get('loc', 'N/A')}\n", "info")
            result_text.insert(END, f"Postal: {ip_data.get('postal', 'N/A')}\n", "info")
            result_text.insert(END, f"Timezone: {ip_data.get('timezone', 'N/A')}\n", "info")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch IP information: {e}")

def open_ip_lookup_window():
    global ip_lookup_window
    if ip_lookup_window is None or not Toplevel.winfo_exists(ip_lookup_window):
        ip_lookup_window = Toplevel(root)
        ip_lookup_window.title("IP Lookup Tool")
        ip_lookup_window.geometry("500x500")
        ip_lookup_window.resizable(False, False)
        ip_lookup_window.config(bg=bg_color)

        # IP Label and Entry
        ip_label = Label(ip_lookup_window, text="Enter IP Address:", bg=bg_color, fg=font_color)
        ip_label.grid(row=0, column=0, padx=5, pady=5)
        global ip_entry
        ip_entry = Entry(ip_lookup_window, width=30)
        ip_entry.grid(row=0, column=1, padx=5, pady=5)

        # Lookup Button
        lookup_button = Button(ip_lookup_window, text="Lookup", command=ip_lookup, bg=bg_color, fg=font_color)
        lookup_button.grid(row=1, column=1, pady=10)

        # Result Display
        global result_text
        result_text = Text(ip_lookup_window, height=20, width=55, bg="black", fg="white", wrap=WORD)
        result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Add custom tags for styling the result
        result_text.tag_config("error", foreground="red")
        result_text.tag_config("info", foreground="green")

    else:
        ip_lookup_window.lift()


root.mainloop()