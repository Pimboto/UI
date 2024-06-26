import subprocess
import re
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Diccionario de mapeo de identificadores de producto a nombres de modelos específicos
MODEL_MAP = {
    "iPhone10,1": "iPhone 8",
    "iPhone10,2": "iPhone 8 Plus",
    "iPhone10,3": "iPhone X (GSM)",
    "iPhone10,4": "iPhone 8",
    "iPhone10,5": "iPhone 8 Plus",
    "iPhone10,6": "iPhone X (Global)",
    "iPhone11,2": "iPhone XS",
    "iPhone11,4": "iPhone XS Max",
    "iPhone11,6": "iPhone XS Max",
    "iPhone11,8": "iPhone XR",
    "iPhone12,1": "iPhone 11",
    "iPhone12,3": "iPhone 11 Pro",
    "iPhone12,5": "iPhone 11 Pro Max",
    "iPhone12,8": "iPhone SE (2nd generation)",
    "iPhone13,1": "iPhone 12 mini",
    "iPhone13,2": "iPhone 12",
    "iPhone13,3": "iPhone 12 Pro",
    "iPhone13,4": "iPhone 12 Pro Max",
    "iPhone14,4": "iPhone 13 mini",
    "iPhone14,5": "iPhone 13",
    "iPhone14,2": "iPhone 13 Pro",
    "iPhone14,3": "iPhone 13 Pro Max",
    "iPhone14,6": "iPhone SE (3rd generation)",
    "iPhone15,2": "iPhone 14",
    "iPhone15,3": "iPhone 14 Plus",
    "iPhone15,4": "iPhone 14 Pro",
    "iPhone15,5": "iPhone 14 Pro Max",
    # Agrega más modelos según sea necesario
}

current_udid = None

def get_udid():
    result = subprocess.run(["idevice_id", "-l"], stdout=subprocess.PIPE)
    udid = result.stdout.decode("utf-8").strip()
    return udid

def get_device_info(udid):
    try:
        result = subprocess.run(["ideviceinfo", "-u", udid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            error_message = result.stderr.decode("utf-8").strip()
            handle_errors(error_message)
            return None, None
        
        info = result.stdout.decode("utf-8")
        model_identifier_match = re.search(r'ProductType: (.+)', info)
        if model_identifier_match:
            model_identifier = model_identifier_match.group(1).strip()
            model = MODEL_MAP.get(model_identifier, "Modelo desconocido")
        else:
            model = "Modelo no encontrado"
        return model_identifier, model
    except Exception as e:
        info_label.config(text=f"Error: {str(e)}")
        return None, None

def handle_errors(error_message):
    if "Password protected" in error_message:
        info_label.config(text="Desbloquee su iPhone")
    elif "Pairing dialog response pending" in error_message:
        info_label.config(text="Acepte el emparejamiento en su iPhone")
    else:
        info_label.config(text=f"Error: {error_message}")

def update_device_info():
    global current_udid
    udid = get_udid()
    if udid and udid != current_udid:
        current_udid = udid
        model_identifier, model = get_device_info(udid)
        if model_identifier and model:
            info_label.config(text=f"UDID: {udid}\nModelo: {model}")
            update_device_image(model_identifier)
    elif not udid:
        current_udid = None
        info_label.config(text="Connect device...")
        image_label.config(image='')  # Ocultar la imagen

def update_device_image(model_identifier):
    try:
        img = Image.open(f'assets/images/{model_identifier}.png')
        img = img.resize((200, 400), Image.LANCZOS)  # Redimensionar la imagen
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img  # Mantener una referencia a la imagen
    except FileNotFoundError:
        image_label.config(image='')  # Ocultar la imagen si no se encuentra el archivo

def monitor_device():
    while True:
        update_device_info()
        time.sleep(1)  # Verificar cada 1 segundo

# Crear la ventana principal
root = tk.Tk()
root.title("Device Info")

# Crear el label de información
info_label = tk.Label(root, text="Connect device...", font=("Helvetica", 16))
info_label.pack(pady=20)

# Crear el label de imagen
image_label = tk.Label(root)
image_label.pack(pady=20)

# Iniciar el monitoreo en un hilo separado para no bloquear la interfaz gráfica
monitor_thread = threading.Thread(target=monitor_device, daemon=True)
monitor_thread.start()

# Ejecutar la aplicación
root.mainloop()