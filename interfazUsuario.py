from tkinter import *
from statistics import mean
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter import ttk
import threading
import time
import serial
import subprocess
import socket

IPSERVER  = "192.168.1.10"
PORTSERVER = 8000

def get_user_temperature():
    global desired_temperature
    global accepted_temperature
    desired_temperature = desiredtemperature_entry.get().strip()
    if not desired_temperature:
       messagebox.showerror("Error", "No introdujiste ninguna temperatura.")
       return
    else:
        number_temperature = int(desired_temperature)
        if number_temperature > 40:
            messagebox.showerror("Error", "Esa temperatura está fuera de los límites permitidos.")
            return
    messagebox.showinfo("Temperatura aceptada", "La temperatura fue aceptada. Inicia el proceso cuando desees.")
    accepted_temperature = True

def start_program():
    if not accepted_temperature:
        messagebox.showerror("Error", "La temperatura aún no ha sido introducida o validada.")
        return

    # Execute the command
    threatUpload = threading.Thread(target = upload_code)
    threatUpload.start()
    labelCodigo.config(text = "Proceso iniciado. Iniciando conexión con el servidor.")
    root.after(10000, func = lambda: create_client_socket(IPSERVER, PORTSERVER))

def upload_code():
    command = "ampy --port COM4 run code.py"
    process = subprocess.Popen(command, shell=True)
    process.wait()


def create_client_socket(IP, port):

    # create socket object
    global client_socket
    global labelCodigo
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    try:
        client_socket.connect((IP, port))
        labelCodigo.config(text = "Conexión establecida. Los sensores empezarán a funcionar y el programa se regulará automáticamente.")
        global continuar_ciclo
        continuar_ciclo = True
        root.after(3000, program_cycle)
    except socket.error:
        messagebox.showerror("Error", "No se pudo establecer la conexión con el servidor.")
        labelCodigo.config(text = "Introduce la temperatura deseada.\n Después pulsa el botón para iniciar el proceso.")

def program_cycle():

    global client_socket
    global continuar_ciclo

    def update_temperature():
        global obtainTemperature
        if obtainTemperature:
            global sensor_temperatures
            obtain_temperature(client_socket)
            # show the temperatures inside the thread
            show_temperature(sensor_temperatures)
            print("Mis temperaturas: " + str(sensor_temperatures))
    
    print("Empezando hilo")
    threadTemperature = threading.Thread(target=update_temperature)
    threadTemperature.start()

    global sensor_temperatures

    while len(sensor_temperatures) == 0:
        print("Esperando temperaturas del hilo")
    
    temperaturesMean = mean(sensor_temperatures)
    if temperaturesMean > float(desired_temperature):
        pass
        print("Actualizar código")
        global obtainTemperature
        global client_socket
        obtainTemperature = False
        threadUploadCode = threading.Thread(target = lambda: update_code(temperaturesMean, float(desired_temperature)))
        threadUploadCode.start()

    if continuar_ciclo:
        root.after(1, program_cycle)

def obtain_temperature(socket):
    print("Obtiendo temperaturas del servidor: ")
    try:
        # unpack the temperature data using struct
        temperature_string = socket.recv(1024).decode()
        temperatures = [float(temp) for temp in temperature_string.split(",")]
        # print the temperatures
        global sensor_temperatures
        sensor_temperatures = temperatures

    except KeyboardInterrupt:
        # close the connection and exit the program when Ctrl+C is pressed
        socket.close()
        print("\nProgram terminated by user.")

def show_temperature(temperatures):

    # Delete any existing temperature bar in the canvas
    myCanvas.delete("all")
    initial_x = 20
    initial_y = 300
    width = 50
    dif_x = 90
    i = 0

    for temp in temperatures:
        x1 = initial_x + dif_x * i
        x2 = x1 + width
        # Calculate the temperature bar height based on the temperature value
        bar_height = int((temp - 19) * 5)
        
        # Choose a color based on the temperature value
        if temp > 20 and temp <= 25:
            color_index = 0
        elif temp > 26 and temp <= 33:
            color_index = 1
        else:
            color_index = 2

        color = colors[color_index]
        
        # Draw the temperature bar
        myCanvas.create_rectangle(x1, initial_y - bar_height, x2, initial_y, fill=color)
        texto = textSensores[i] + " : " + str(int(temp)) + " °C"
        myCanvas.create_text(x1 + 25, 100, text = texto)
        i += 1


def stop_process(process, boton, label):
    process.kill()
    boton["state"] = tk.NORMAL
    label.config(text = "Presiona el botón para subir o actualizar el código al ESP32." )

def update_code(temp, threshold):
    
    archivoCodigo = open("./server.py", "w")
    
    if temp > threshold:
        tiempo = 0.5
    elif temp < threshold:
        tiempo = 2

    codigo = f"from machine import Pin\nimport time\nrelay_pin_2 = Pin(2, Pin.OUT)\nwhile True:\n\trelay_pin_2.value(1)\n\ttime.sleep({tiempo})\n\trelay_pin_2.value(0)\n\ttime.sleep({tiempo})"

    archivoCodigo.write(codigo)
    command = "ampy --port COM4 run code.py"
    result = subprocess.run(command, shell=True)
    print(result)
    return

#ranges 
#20 - 25 : blue
#26 - 33 : orange
#34 - 40 : red

colors = ["blue", "orange", "red"]
textSensores = ["Sensor 1", "Sensor 2","Sensor 3", "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7", "Sensor 8"]

root = ThemedTk(theme="blue")
style = ttk.Style(root)
root.geometry("960x740")
stop_event = threading.Event()
root.title("Interfaz Gráfica del aire acondicionado")
labelCodigo = tk.Label(root, text="Introduce la temperatura deseada.\n Después pulsa el botón para iniciar el proceso.")
labelCodigo.pack(pady=10)

botonEmpezarProceso = ttk.Button(root, text="Comenzar proceso", command=start_program)
botonEmpezarProceso.pack(pady = 10)
# botonDetenerCodigo = ttk.Button(root, text="Detener ejecución", state="disabled")
# botonDetenerCodigo.pack(pady=10)
# botonActualizarCodigo = ttk.Button(root, text="Actualizar código", command = lambda: actualizarCodigo(controladores))
# botonActualizarCodigo.pack(pady = 10)

peltier1 = IntVar()
peltier2 = IntVar()

controladores = [peltier1, peltier2] 

checkPeltier1 = Checkbutton(text="Peltier 1", variable=peltier1, onvalue=1, offvalue=0)
checkPeltier1.place(x=10, y=210)

checkPeltier2 = Checkbutton(text="Peltier 2", variable=peltier2, onvalue=1, offvalue=0)
checkPeltier2.place(x=10, y=235)

gas_detection_label = Label(root, text="Detección de gas: ")
gas_detection_label.place(x=800, y=10)

gas_detection = IntVar()
gas_detection.set(0)

rb_gas_off = Radiobutton(root, text="No Detectado", variable=gas_detection, value=0, state="disabled")
rb_gas_off.place(x=800, y=30)

rb_gas_on = Radiobutton(root, text="Detectado", variable=gas_detection, value=1, state="disabled")
rb_gas_on.place(x=800, y=50)

flame_detection_label = Label(root, text="Detección de flama: ")
flame_detection_label.place(x=800, y=70)

flame_detection = IntVar()
flame_detection.set(0)

rb_flame_off = Radiobutton(root, text="No Detectado", variable=flame_detection, value=0, state="disabled")
rb_flame_off.place(x=800, y=90)

rb_flame_on = Radiobutton(root, text="Detectado", variable=flame_detection, value=1, state="disabled")
rb_flame_on.place(x=800, y=110)

desired_temperature = 0
accepted_temperature = False
client_socket = 0
sensor_temperatures = []
continuar_ciclo = False
obtainTemperature = True

desiredtemperature_label = tk.Label(root, text="Temperatura deseada: (°C)")
desiredtemperature_label.place(x = 650, y = 200)
desiredtemperature_entry = tk.Entry(root, width = 5)
desiredtemperature_entry.place(x = 800, y = 200)
botonSubirTemperatura = ttk.Button(root, text="OK", width = 2.5, command = get_user_temperature)
botonSubirTemperatura.place(x = 840, y = 200)

myCanvas = tk.Canvas(root, bg="white", height=300, width=750)
myCanvas.pack(side = LEFT)
root.mainloop()