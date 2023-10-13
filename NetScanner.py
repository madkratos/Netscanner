#!bin/python3
import customtkinter            # agregado para la gui moderna
import subprocess               # agregado para ip procesing
import ipaddress                # agregado para ip rage manage
import threading                # agregado para threading
import socket                   # agregado para el manejo de la ip y la subnetmask para optener el rango de la red 
import psutil                   # agregado para obener la subnet mask necesario instalar con pip install psutil
import tkinter as tk            # agregado para gui
import concurrent.futures       # agregado para thread pooling
from tkinter import filedialog  # agregado para guardado de texto
import customtkinter as  ct     # agregado para la lista de interface
class NetScanner:
# funcion para la GUI
    def __init__(self, root,authenticated_username):
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.geometry('350x500+800+200')
        root.title('NetScanner')
        self.root.resizable(width=0, height=0)


        self.title_label =customtkinter.CTkLabel(master=root, text="Ingrese un rango de red en formato CIDR\n(ej: 192.168.0.0/24)\n", font=customtkinter.CTkFont(size=15))
        self.title_label.place(x=40, y=26)

        self.detect_ip_label = customtkinter.CTkLabel(master=root, text="",font=customtkinter.CTkFont(size=10))
        self.detect_ip_label.place(x=20, y=0)

        self.ip_entry = customtkinter.CTkEntry(master=root)
        self.ip_entry.place(x=110, y=70)

        self.interfaces = ["Ethernet", "Wi-Fi"]
        self.interface_dropdown = ct.CTkComboBox(master=root, values=self.interfaces,width=80,height=15)
        self.interface_dropdown.set("Interface")  
        self.interface_dropdown.place(x=5, y=140)

        self.scan_button = customtkinter.CTkButton(master=root, text="Scan Network", font=customtkinter.CTkFont(size=13),width=20,height=13,corner_radius=8, command=self.scan_button_clicked)
        self.scan_button.place(x=10, y=72)

        self.pause_button = customtkinter.CTkButton(master=root, text="Detectar",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.detect_button_clicked)
        self.pause_button.place(x=5, y=110)  

        self.pause_button = customtkinter.CTkButton(master=root, text="Detener", font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.stop_button_clicked)
        self.pause_button.place(x=100, y=110)  

        self.reset_button = customtkinter.CTkButton(master=root, text="Reset", font=customtkinter.CTkFont(size=13),width=20,height=10, command=self.reset_button_clicked)
        self.reset_button.place(x=170, y=110) 

        self.sort_button = customtkinter.CTkButton(master=root, text="Ordenar", font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.sort_button_clicked)
        self.sort_button.place(x=230, y=110)  

        self.save_button = customtkinter.CTkButton(master=root, text="Guardar", font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.save_button_clicked)
        self.save_button.place(x=280, y=50)

        self.load_button = customtkinter.CTkButton(master=root, text="Cargar", font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.read_button_clicked)
        self.load_button.place(x=280, y=80) 

        self.back_button = customtkinter.CTkButton(master=root, text="Atras",fg_color="#3D59AB", font=customtkinter.CTkFont(size=13),width=20,height=10, command=self.back_button_clicked)
        self.back_button.place(x=290, y=145)

        self.result_label =customtkinter.CTkLabel(master=root, text="", font=customtkinter.CTkFont(size=10))
        self.result_label.place(x=100, y=150) 

        self.progress_bar = customtkinter.CTkProgressBar(self.root, width=150, height=12)
        self.progress_bar.place(x=100, y=140)
        self.progress_bar.set(0)

        self.progress_label =customtkinter.CTkLabel(self.root, text="0%", font=customtkinter.CTkFont(size=10))
        self.progress_label.place(x=255, y=132)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(master=root, width=310, height=300)
        self.scrollable_frame.place(x=10, y=180)

        self.hosts_text = tk.Text(master=self.scrollable_frame, height=19, width=41,bg="#3B3B3B",fg="white")
        self.hosts_text.pack()
        self.scan_thread = None
        self.scan_stopped = False


# funcion para restaurar la ventana 
    def restore_dashboard(self):
        self.dash_window.destroy()

# funcion para el boton de guardado
    def save_button_clicked(self):
        lines = self.hosts_text.get("1.0", tk.END).splitlines()

        if not lines:
            self.result_label.configure(text="No hay resultados para guardar.")
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

            self.result_label.configure(text="    Guardado")
        else:
            self.result_label.configure(text="Operación cancelada.")


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
                self.result_label.configure(text="Lista no encontrada.")
        else:
            self.result_label.configure(text="No se eligio la lista")


# funcion para el boton de atras
    def back_button_clicked(self):
        if self.authenticated_username == "admin":
            self.open_dashboard()
        else:
            self.open_dashboard_user()


# funcion para crear la ventana del llamado dashboard de usuario
    def open_dashboard_user(self):
        import customtkinter  
        from DashboardUser import DashboardUser  
        self.dash_window = customtkinter.CTkToplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        dash_user = DashboardUser(self.dash_window,self.authenticated_username)

# funcion para crear la ventana del llamado dashboard
    def open_dashboard(self):
        import customtkinter  
        from Dashboard import Dashboard  
        self.dash_window = customtkinter.CTkToplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        dash = Dashboard(self.dash_window,self.authenticated_username)


# funcion generar el rango de ip cidr
    def generate_cidr(self):
        interface_name = self.interface_dropdown.get()
        try:
            interfaces = psutil.net_if_addrs()
            if interface_name in interfaces:
                for addr in interfaces[interface_name]:
                    if addr.family == socket.AF_INET:
                        ip, subnet_mask = addr.address, addr.netmask
                        break
                else:
                    self.result_label.configure(text=f"Interfaz '{interface_name}' no encontrada")
                    return None
                
                try:
                    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
                    self.detect_ip_label.configure(text=f"Ip: {ip}\t\t\tSubnet Mask: {subnet_mask}")
                    return str(network)
                except ValueError as e:
                        self.result_label.configure(text=f"Error:{e}")
                        return None
            else:
                self.result_label.configure(text=f"Interfaz '{interface_name}' no encontrada")
                return None
        except Exception as e:
            self.result_label.configure(text=f"Ocurrio un error: {e}")
            return None
          
# funcion para el boton de generar rango
    def detect_button_clicked(self):
        cidr_format = self.generate_cidr()
        if cidr_format:
             self.ip_entry.delete(0, tk.END) 
             self.ip_entry.insert(0, cidr_format)
             self.result_label.configure(text="")
        else:
            self.result_label.configure(text="\tFallo al generar")


# funcion para el boton de escaneado
    def scan_button_clicked(self):
        self.scan_stopped = False
        ip_subnet = self.ip_entry.get()
        self.scan_thread = threading.Thread(target=self.perform_scan, args=(ip_subnet,))
        self.scan_thread.start()

# funcion para el boton de reset
    def reset_button_clicked(self):
        self.ip_entry.delete(0, tk.END)
        self.progress_bar.configure(progress_color="#1874CD") 
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.result_label.configure(text="")
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
    def stop_button_clicked(self):
        self.scan_stopped = not self.scan_stopped
        if self.scan_stopped:
            self.progress_bar.configure(progress_color="red")
            self.result_label.configure(text="      Escaneo pausado")
            
    
# funcion que realiza el escan
    def perform_scan(self, ip_subnet):
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.hosts_text.delete("1.0", tk.END)

        try:
            network = ipaddress.ip_network(ip_subnet, strict=False)
        except ValueError:
            self.result_label.configure(text="Formato de ip no valido.")
            return

        total_hosts = len(list(network.hosts()))
        scanned_hosts = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(self.scan_host, str(ip)): ip for ip in network.hosts()}
                for future in concurrent.futures.as_completed(futures):
                    if self.scan_stopped:
                        for task in futures:
                            task.cancel()
                        self.result_label.configure(text="      Escaneo detenido")
                        return
                    ip = futures[future]
                    scanned_hosts += 1
                    progress = int((scanned_hosts / total_hosts) * 100)
                    self.progress_bar.set(progress/100)
                    self.progress_label.configure(text=f"{progress}%")
        if not self.scan_stopped:
            self.progress_bar.configure(progress_color="green")
            self.progress_bar.set(1)
            self.progress_label.configure(text="100%")

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
    root =customtkinter.CTk()
    scanner = NetScanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()


