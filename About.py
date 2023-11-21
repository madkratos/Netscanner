import tkinter as tk
import customtkinter
import threading

#Funcion para el centrado universal de la ventan
def center_window(root, width, height):
    '''Funcion para el centrado universal de la ventan'''
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.resizable(width=0, height=0)

class About:
#funcion de la GUI 
    def __init__(self, root, authenticated_username):
        ''' funcion de la GUI '''
        self.root = root
        self.authenticated_username = authenticated_username
        self.root.title('Sobre net scanner')
        width, height = 350, 500
        self.root.geometry(f'{width}x{height}')
        center_window(self.root, width, height)


        self.frame = customtkinter.CTkFrame(master=root, width=330, height=70, corner_radius=10)
        self.frame.place(x=10, y=10)

        self.title = customtkinter.CTkLabel(master=self.frame, text=f"Acerca de NetScanner", font=customtkinter.CTkFont(size=25))
        self.title.place(x=10, y=10)

        self.atras = customtkinter.CTkButton(master=self.frame, text="Atras", command=self.back_button_clicked,
                                             width=10, height=30, corner_radius=8, fg_color="#3D59AB")
        self.atras.place(x=275, y=10)

        self.net_text = tk.Text(root, height=20, width=42, bg="black", fg="#16FF00")
        self.net_text.place(x=4, y=90)
        self.message("NetScanner: ",
                     "Compatible con Windows y detecta interfaces de red inalámbricas y cableadas. ",
                     "Identifica dispositivos que responden a paquetes ICMP \n\nSoporta todos los rangos CIDR \n\nEs capaz de guardar los "
                     "datos de las direcciones escaneadas y de leerlos \n\nCuenta con un gestor de tareas para poder realizar los escaneos."
                     "\n\nVersión del programa 3.1.")


    def message(self, title, message, description):
        self.net_text.delete(1.0, tk.END)
        self.net_text.insert(tk.END, title + "\n\n" + message + "\n\n" + description)

# funcion para restaurar la ventana 
    def restore_dashboard(self):
        '''funcion para restaurar la ventana '''
        self.dash_window.destroy()

# funcion para crear la ventana del llamado dashboard de usuario
    def open_dashboard_user(self):
        '''funcion para crear la ventana del llamado dashboard de usuario'''
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
        '''funcion para crear la ventana del llamado dashboard'''
        import customtkinter  
        from Dashboard import Dashboard  
        self.dash_window = customtkinter.CTkToplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        dash = Dashboard(self.dash_window,self.authenticated_username)

# funcion para el boton de atras
    def back_button_clicked(self):
        '''funcion para el boton de atras'''
        if self.authenticated_username == "admin":
            self.open_dashboard()
        else:
            self.open_dashboard_user()

# funcion para la ventana principal 
def main():
    '''funcion para la ventana principal'''
    root = customtkinter.CTk()
    aboaut = About(root)  
    root.mainloop()

if __name__ == "__main__":
    main()
