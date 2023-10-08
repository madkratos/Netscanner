import customtkinter                          # agregado para la gui moderna
import tkinter as tk                          #Libreria para crear los diseños y la interfaz
import tkinter.messagebox                     #libreria para mensajes de error y demas
from DatabaseManager import DatabaseManager   # agregado modificar valores de la base de datos
class Register:
# Función para para contruir la ventana con diseños desde la ventana login
    def __init__(self, root,authenticated_username):
        self.db_manager = DatabaseManager()
        self.db_manager.create_user_tables()
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.title('Registrar Usuario.')
        self.root.geometry('350x500+800+200')
        
        self.frame = customtkinter.CTkFrame(master=root,width=320,height=500,corner_radius=10)
        self.frame.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.title = customtkinter.CTkLabel(master=self.frame,text="Registrar Usuario",font=customtkinter.CTkFont(size=35))
        self.title.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)


        self.user_label = customtkinter.CTkLabel(master=self.frame,text="Usuario:",font=customtkinter.CTkFont(size=15))
        self.user_label.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)

        self.user_entry = customtkinter.CTkEntry(master=self.frame,width=200,height=30,corner_radius=10)
        self.user_entry.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.password_label = customtkinter.CTkLabel(master=self.frame,text="Contraseña:",font=customtkinter.CTkFont(size=15))
        self.password_label.place(relx=0.2, rely=0.7,anchor=tkinter.CENTER)

        self.pass_entry = customtkinter.CTkEntry(master=self.frame,width=200,height=30,corner_radius=10,show="*")
        self.pass_entry.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)


        self.register = customtkinter.CTkButton(master =self.frame, text="Registrase", command=self.register_user)
        self.register.place(x=160, y=460, anchor=customtkinter.CENTER)

        self.cerrar = customtkinter.CTkButton(master =root, text="volver",fg_color="#3D59AB", command=self.back_button_clicked)
        self.cerrar.place(x=175, y=450, anchor=customtkinter.CENTER)


#Funcion para centrar las ventanas
    def centrar_ventana(root,aplicacion_ancho,aplicacion_largo):    
        pantall_ancho = root.winfo_screenwidth()
        pantall_largo = root.winfo_screenheight()
        x = int((pantall_ancho/2) - (aplicacion_ancho/2))
        y = int((pantall_largo/2) - (aplicacion_largo/2))
        return root.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
    
#Funcion para eliminar la ventana registrarse al presionar el boton volver
    def restore_dashboard(self):
        self.login_window.destroy()
    
#Funcion para volver a inicio de sesion al presionar el botos volver 
    def back_button_clicked(self):
        from Rols import Rols  
        self.login_window = customtkinter.CTkToplevel(self.root)
        self.root.withdraw()
        self.login_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        rol = Rols(self.login_window,self.authenticated_username)

        
# funcion para el boton de crear usuario
    def register_user(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if username and password:
            if self.db_manager.user_exists(username):   
                tkinter.messagebox.showerror(title="error", message="El usuario ingresado ya existe.")
                self.user_entry.delete(0, tk.END)
                self.pass_entry.delete(0, tk.END)
                self.user_entry.focus()
            else:
                option= tkinter.messagebox.askyesno('Confirme la operacion', 'Esta seguro de querer agregar este usuario?') 
                if option == True:
                    self.db_manager.insert_user(username, password)
                    tkinter.messagebox.showinfo(title="Registro exitoso.", message="Usuario registrado con exito.")
                    self.user_entry.delete(0, tk.END)
                    self.pass_entry.delete(0, tk.END)
                    self.user_entry.focus()
                else:
                    tkinter.messagebox.showinfo(title="Operacion cancelada.", message="Usuario no registrado.")
                    self.user_entry.delete(0, tk.END)
                    self.pass_entry.delete(0, tk.END)
                    self.user_entry.focus()
        else:
            return tkinter.messagebox.showerror(title="error", message="No has ingresado nada en los campos.")


def main():
    root = customtkinter.CTk()
    register = Register(root)
    root.mainloop()

if __name__ == "__main__":
    main()
