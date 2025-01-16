from tkinter import *
from PIL import Image, ImageTk
import time
from tkinter import PhotoImage
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
from tkinter import Menu, messagebox ,ttk , filedialog
from scapy.all import ARP, Ether, srp
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import re
from datetime import datetime
from netra import *
import random
from itertools import cycle
import tkinter as tk
from colorama import init, Fore
import requests
import psutil
import ipaddress

from tkinter import ttk
from tkinter import Tk
from reportlab.lib import colors
from tkinter.messagebox import showerror, showinfo
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


#functions that we are using in the netra 

# Function to get the local IP address
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Function to get public IP address
def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "No internet access !"