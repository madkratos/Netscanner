import tkinter as tk  # agregado para gui
import customtkinter  # nuevo agregado para la nueva gui instalado con "pip3 install customtkinter"
import threading      # nuevo agregado para manejar los threts para la impresion
import time           # nuevo agregado para medir el tiempo de impresion

#Funcion para el centrado universal de la ventan
def center_window(root, width, height):
    '''Funcion para el centrado universal de la ventan'''
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.resizable(width=0, height=0)

class Dashboard:
    #funcion para la GUI
    def __init__(self, root,authenticated_username):
        '''funcion para la GUI'''
        self.root = root
        self.authenticated_username = authenticated_username
        self.root.title('Dashboard')
        width, height = 350, 500
        self.root.geometry(f'{width}x{height}')
        center_window(self.root, width, height)

        self.frame = customtkinter.CTkFrame(master=root,width=330,height=70,corner_radius=10)
        self.frame.place(x=10, y=10)

        self.title = customtkinter.CTkLabel(master=self.frame,text=f"Hola Admin!",font=customtkinter.CTkFont(size=35))
        self.title.place(x=10, y=10)

        self.login = customtkinter.CTkButton(master =self.frame, text="Logout", command=self.logout_button_clicked,width=10,height=30,corner_radius=8,fg_color="#3D59AB")
        self.login.place(x=260 ,y=10)

        self.login = customtkinter.CTkButton(master =root, text="Realizar Scan", command=self.scan_button_clicked,width=10,height=30,corner_radius=8)
        self.login.place(relx=0.1, rely=0.2)

        self.login = customtkinter.CTkButton(master =root, text="Rol de Usuarios", command=self.usuario_button_clicked,width=10,height=30,corner_radius=8)
        self.login.place(relx=0.39, rely=0.2)

        self.login = customtkinter.CTkButton(master =root, text="Tareas", command=self.task_button_clicked,width=10,height=30,corner_radius=8)
        self.login.place(relx=0.72, rely=0.2)
        
        self.net_text = tk.Text(root, height=20, width=42,bg="black",fg="#7FFF00")
        self.net_text.place(x=4, y=160)

        self.message_thread = threading.Thread(target=self.message, args=[["Bienvenido a ",
            """  _   _          _   
 | \ | |        | |  
 |  \| |   ___  | |_ 
 | . ` |  / _ \ | __|
 | |\  | |  __/ | |_ 
 |_| \_|  \___|  \__|
 _____                                 
/ ____|                                
| (___   ___ __ _ _ __  _ __   ___ _ __ 
 \___ \ / __/ _` | '_ \| '_ \ / _ | '__|
 ____) | (_| (_| | | | | | | |  __| |   
|_____/ \___\__,_|_| |_|_| |_|\___|_|   """,
            "\nNetScanner es un programa para el escaneo de una red por medio de paquetes de ping, es capaz de "
            "manejar rangos de ip en  formato CIDR (classless inter-domain routing) y cubre todos los rangos posibles"]])
        self.message_thread.start()
        

# funcion para el boton de escaneo abre el formulario de escaneo principal
    def scan_button_clicked(self):
        '''funcion para el boton de escaneo abre el formulario de escaneo principal'''
        import customtkinter  
        from NetScanner import NetScanner  
        self.scanner_window = customtkinter.CTkToplevel(self.root)
        self.root.withdraw()
        self.scanner_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        scanner = NetScanner(self.scanner_window,self.authenticated_username)

# funcion para restaurar la ventana 
    def restore_dashboard(self):
        '''funcion para restaurar la ventana '''
        self.scanner_window.destroy()
        self.login_window.destroy()


# funcion para el boton de logout
    def logout_button_clicked(self):
        '''funcion para el boton de logout'''
        import customtkinter  
        from Login import Login  
        self.login_window = customtkinter.CTkToplevel(self.root)
        self.root.withdraw()
        self.login_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)
        login = Login(self.login_window)


# funcion la impresion del mensaje sobre el programa
    def print_message(self, text):
        '''funcion la impresion del mensaje sobre el programa'''
        for char in text:
            self.net_text.insert(tk.END, char)
            self.net_text.see(tk.END)  
            time.sleep(0.01)  

# funcion para el mensaje sobre el programa
    def message(self, lines):
        '''funcion para el mensaje sobre el programa'''
        self.net_text.config(state=tk.NORMAL)
        self.net_text.delete("1.0", tk.END)  
        for line in lines:
            self.print_message(line + "\n")
        self.net_text.config(state=tk.DISABLED)

# funcion para el boton de rol de usuarios
    def usuario_button_clicked(self):
        '''funcion para el boton de rol de usuarios'''
        import customtkinter  
        from Rols import Rols  
        self.rol_window = customtkinter.CTkToplevel(self.root)
        self.root.withdraw()
        self.rol_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        rol = Rols(self.rol_window,self.authenticated_username)

# funcion para el boton de tareas
    def task_button_clicked(self):
        '''funcion para el boton de tareas'''
        import customtkinter  
        from Tasks import Tasks  
        self.task_window = customtkinter.CTkToplevel(self.root)
        self.root.withdraw()
        self.task_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        task = Tasks(self.task_window,self.authenticated_username)

# funcion para la ventana principal de dashboard
def main():
    '''funcion para la ventana principal de dashboard'''
    root = customtkinter.CTk()
    dash= Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()







