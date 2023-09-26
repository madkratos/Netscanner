#!bin/python3
import subprocess                   # agregado para ip procesing
import ipaddress                    # agregado para ip rage manage
import threading                    # agregado para threading
import socket                       # agregado para el manejo de la ip y la subnetmask para optener el rango de la red 
import psutil                       # agregado para obener la subnet mask necesario instalar con pip install psutil
import tkinter as tk                # agregado para gui
from tkinter import  ttk            # agregado para la lista de interfaz
import concurrent.futures           # agregado para thread pooling
from tkinter import filedialog      # agregado para guardado de texto
class NetScanner:
# funcion para la GUI
    def __init__(self, root,authenticated_username):
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.geometry('350x500+800+200')
        root.title('NetScanner')
        self.root.config(bg='#fff')
        self.root.resizable(width=0, height=0)

        self.title_label = tk.Label(root, text="Ingrese un rango de red en formato CIDR\n(ej: 192.168.0.0/24)\n", font=('Times', 15), fg="white", bg='#0D7FD8',padx=11,pady=5)
        self.title_label.place(x=0, y=23)

        self.detect_ip_label = tk.Label(root, text="",font=('Times', 10), fg="#0D7FD8", bg='white')
        self.detect_ip_label.place(x=20, y=1)

        self.ip_entry = tk.Entry(root)
        self.ip_entry.place(x=130, y=75,height=20)

        self.scan_button = tk.Button(root, text="Scan Network", font=('Times', 11, 'bold'), bg='#fff', bd=2, fg="#0D7FD8", command=self.scan_button_clicked)
        self.scan_button.place(x=10, y=71)

        self.interfaces = ["Ethernet", "Wi-Fi"]
        self.selected_interface = tk.StringVar()
        self.selected_interface.set("Interface")  
        self.interface_dropdown = ttk.Combobox(root, textvariable=self.selected_interface, values=self.interfaces, state="readonly",width=8)
        self.interface_dropdown.place(x=5, y=150)

        self.pause_button = tk.Button(root, text="Detectar",font=('Times', 11, 'bold'), bg='#fff', bd=2, fg="#0D7FD8", command=self.detect_button_clicked)
        self.pause_button.place(x=5, y=110)  

        self.pause_button = tk.Button(root, text="Pausa", font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.pause_button_clicked)
        self.pause_button.place(x=80, y=110)  

        self.reset_button = tk.Button(root, text="Reset", font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.reset_button_clicked)
        self.reset_button.place(x=140, y=110) 

        self.sort_button = tk.Button(root, text="Ordenar", font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.sort_button_clicked)
        self.sort_button.place(x=200, y=110)  

        self.save_button = tk.Button(root, text="Guardar", font=('Times', 11, 'bold'), bg='#fff', bd=2, fg="#0D7FD8", command=self.save_button_clicked)
        self.save_button.place(x=280, y=71)

        self.load_button = tk.Button(root, text="Cargar", font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.read_button_clicked)
        self.load_button.place(x=280, y=110) 

        self.back_button = tk.Button(root, text="Atras", font=('Times', 11, 'bold'), bg='#D8300D', bd=2, fg="#fff", command=self.back_button_clicked)
        self.back_button.place(x=290, y=145)

        self.result_label = tk.Label(root, text="", font=('Times', 10), fg="#0D7FD8", bg='#fff', pady=5)
        self.result_label.place(x=100, y=150) 

        self.hosts_text = tk.Text(root, height=20, width=41)
        self.hosts_text.place(x=4, y=180)
        self.paused = False
        
        scrollbar = tk.Scrollbar(root, command=self.hosts_text.yview)
        scrollbar.place(x=330, y=180, height=320) 
        self.hosts_text.config(yscrollcommand=scrollbar.set)

# funcion para restaurar la ventana 
    def restore_dashboard(self):
        self.dash_window.destroy()


# funcion para el boton de guardado
    def save_button_clicked(self):
        lines = self.hosts_text.get("1.0", tk.END).splitlines()

        if not lines:
            self.result_label.config(text="No hay resultados para guardar.")
            return

        initial_dir = "C:/Users/*/Downloads"  

        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")])
        
        if file_path:
            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(line + '\n')

            self.result_label.config(text="\tGuardado")
        else:
            self.result_label.config(text="Operación cancelada.")


# funcion para el boton de carga
    def read_button_clicked(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Elija un lista",
            filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    saved_scans = file.read()
                    self.hosts_text.delete("1.0", tk.END)  
                    self.hosts_text.insert(tk.END, saved_scans)
            except FileNotFoundError:
                self.result_label.config(text="Lista no encontrada.")
        else:
            self.result_label.config(text="No se eligio la lista")


# funcion para el boton de atras
    def back_button_clicked(self):
        from Dashboard import Dashboard  
        self.dash_window = tk.Toplevel(self.root)  
        self.root.withdraw()
        dash = Dashboard(self.dash_window,self.authenticated_username)
        self.dash_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)


# funcion generar el rango de ip cidr
    def generate_cidr(self):
        interface_name = self.selected_interface.get()
        try:
            interfaces = psutil.net_if_addrs()
            if interface_name in interfaces:
                for addr in interfaces[interface_name]:
                    if addr.family == socket.AF_INET:
                        ip, subnet_mask = addr.address, addr.netmask
                        break
                else:
                    self.result_label.config(text=f"Interfaz '{interface_name}' no encontrada")
                    return None
                
                try:
                    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
                    self.detect_ip_label.config(text=f"Ip: {ip}\t\t        Subnet Mask: {subnet_mask}")
                    return str(network)
                except ValueError as e:
                        self.result_label.config(text=f"Error:{e}")
                        return None
            else:
                self.result_label.config(text=f"Interfaz '{interface_name}' no encontrada")
                return None
        except Exception as e:
            self.result_label.config(text=f"Ocurrio un error: {e}")
            return None
        
            
# funcion para el boton de generar rango
    def detect_button_clicked(self):
        cidr_format = self.generate_cidr()
        if cidr_format:
             self.ip_entry.delete(0, tk.END) 
             self.ip_entry.insert(0, cidr_format)
             self.result_label.config(text="")
        else:
            self.result_label.config(text="\tFallo al generar")


# funcion para el boton de escaneado
    def scan_button_clicked(self):
        self.paused = False 
        ip_subnet = self.ip_entry.get()
        thread = threading.Thread(target=self.perform_scan, args=(ip_subnet,))
        thread.start()

# funcion para el boton de reset
    def reset_button_clicked(self):
        self.ip_entry.delete(0, tk.END) 
        self.result_label.config(text="")
        self.hosts_text.delete("1.0", tk.END)

# funcion para el boton de ordenar
    def sort_button_clicked(self):
        current_text = self.hosts_text.get("1.0", tk.END)
        lines = [line.strip() for line in current_text.splitlines() if line.strip()]
        sorted_lines = sorted(lines, key=lambda x: ipaddress.IPv4Address(x.split()[0]))
        self.hosts_text.delete("1.0", tk.END)
        for line in sorted_lines:
            self.hosts_text.insert(tk.END, line + "\n")
    
    
# funcion para el boton de pausa
    def pause_button_clicked(self):
        self.paused = True
    
# funcion que realiza el escan
    def perform_scan(self, ip_subnet):
        self.result_label.config(text="Escaneo en progreso... 0%")
        self.hosts_text.delete("1.0", tk.END)

        try:
            network = ipaddress.ip_network(ip_subnet, strict=False)
        except ValueError:
            self.result_label.config(text="Formato de ip no valido.")
            return

        total_hosts = len(list(network.hosts()))
        scanned_hosts = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(self.scan_host, str(ip)): ip for ip in network.hosts()}

                for future in concurrent.futures.as_completed(futures):
                    if self.paused:
                        self.result_label.config(text="      Escaneo pausado")
                        break  
                    ip = futures[future]
                    scanned_hosts += 1
                    progress = int((scanned_hosts / total_hosts) * 100)
                    self.result_label.config(text=f"Escaneo en progreso...... {progress}%")
        if not self.paused:
            self.result_label.config(text="       Escaneo completo!")

# funcuion que imprime los ips escaneados que responden
    def scan_host(self, ip):
        if ping_ip(ip):
            self.display_result(ip + " Responde")
        

# funcuion que imprime la lista de ips escaneados
    def display_result(self, message):
        self.hosts_text.insert(tk.END, message + "\n")


# funcion para ping
def ping_ip(ip):
    try:
        output = subprocess.check_output(['ping', '-n', '1', ip], universal_newlines=True)
        if "bytes=32" in output:  
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False


# funcion que da inicio al loop de la GUI 
def main():
    root = tk.Tk()
    scanner = NetScanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()


