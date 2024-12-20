import tkinter as tk
from tkinter import ttk

def open_file():
    print("Open File Clicked")

def save_file():
    print("Save File Clicked")

def exit_app():
    root.quit()

root = tk.Tk()
root.title("Styled Menu Bar")

# Create a style object
style = ttk.Style()
style.configure("TMenu", background="lightgray", relief="flat", font=("Arial", 12))

# Create a menu bar
menu_bar = tk.Menu(root)

# Add File menu
file_menu = tk.Menu(menu_bar, tearoff=0, relief="flat", font=("Arial", 12))
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# Apply the styled menu
menu_bar.add_cascade(label="File", menu=file_menu)

# Add Help menu
help_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 12))
help_menu.add_command(label="About")

# Apply the styled menu
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configure the window to display the menu bar
root.config(menu=menu_bar)

# Get the window width and height for positioning labels
window_width = root.winfo_width()
window_height = root.winfo_height()

# Create "Developed by" label and position it towards the bottom left with some margin
developed_by_label = tk.Label(root, text="Developed by Sonam Tamang", font=("Arial", 8), anchor="w")
developed_by_label.place(x=10, y=window_height - 20)

# Create version label and position it towards the bottom right with some margin
version_label = tk.Label(root, text="Version 1.0", font=("Arial", 8), anchor="e")
version_label.place(x=window_width - 100, y=window_height - 20)

# Update window size to ensure labels are placed correctly
root.update_idletasks()

# Start the Tkinter loop
root.mainloop()
