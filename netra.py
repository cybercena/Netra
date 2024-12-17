from tkinter import *
from PIL import Image, ImageTk
import time
from tkinter import Menu, messagebox ,ttk , filedialog
from scapy.all import ARP, Ether, srp
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import PhotoImage
import socket
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from scapy.all import ARP, Ether, srp
import threading
import requests



#functions that we are using in the netra 

# Function to get the local IP address
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Function to get public IP address
def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unable to fetch"