import tkinter as tk                 #Libreria para crear los diseños y la interfaz
import sqlite3                       #libreria para manejar base de dato
import tkinter.messagebox            #libreria para mensajes de error y demas
from tkinter.font import BOLD        #libreria para poner en negrita la fuente de la interfaz
//fede
class Register:

# Función para para contruir la ventana con diseños desde la ventana login
    def __init__(self, root):
        self.root = root
        self.root.title('Registrar Usuario.')
        self.root.geometry('350x500+800+200')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(width=0, height=0)

        #frame_form
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form
        
        #frame_form_top
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Registrar Usuario",font=('Times', 30), fg="white",bg='#0D7FD8',pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill 
        frame_form_fill = tk.Frame(frame_form,height = 30,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        user_label = tk.Label(frame_form_fill, text="Usuario:", font=('Times', 14) ,fg="black",bg='#fcfcfc', anchor="w")
        user_label.pack(fill=tk.X, padx=20,pady=5)
        self.user_entry = tk.Entry(frame_form_fill, font=('Times', 16))
        self.user_entry.pack(fill=tk.X, padx=20,pady=5)

        correo_label = tk.Label(frame_form_fill, text="Correo:", font=('Times', 14) ,fg="black",bg='#fcfcfc', anchor="w")
        correo_label.pack(fill=tk.X, padx=20,pady=5)
        self.correo_entry = tk.Entry(frame_form_fill, font=('Times', 16))
        self.correo_entry.pack(fill=tk.X, padx=20,pady=5)

        password_label = tk.Label(frame_form_fill, text="Contraseña:", font=('Times', 16),fg="black",bg='#fcfcfc' , anchor="w")
        password_label.pack(fill=tk.X, padx=20,pady=5)
        self.password_entry = tk.Entry(frame_form_fill, font=('Times', 14))
        self.password_entry.pack(fill=tk.X, padx=20,pady=5)
        self.password_entry.config(show="*")

        register = tk.Button(frame_form_fill,text="Registrase",font=('Times', 15,BOLD),bg='#0D7FD8', bd=2,fg="#fff", command=self.agregar_usuario)
        register.pack(fill=tk.X, padx=20,pady=5)

        cerrar = tk.Button(frame_form_fill,text="volver",font=('Times', 15,BOLD),bg='#fff', bd=2,fg="black",command=self.logout_button_clicked)
        cerrar.pack(fill=tk.X, padx=20,pady=5)    

#Funcion para centrar las ventanas
    def centrar_ventana(root,aplicacion_ancho,aplicacion_largo):    
        pantall_ancho = root.winfo_screenwidth()
        pantall_largo = root.winfo_screenheight()
        x = int((pantall_ancho/2) - (aplicacion_ancho/2))
        y = int((pantall_largo/2) - (aplicacion_largo/2))
        return root.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
    
#Funcion para eliminar la ventana registrarse al presionar el boton volver
    def restore_dashboard(self):
        self.dash_window.destroy()
    
#Funcion para volver a inicio de sesion al presionar el botos volver 
    def logout_button_clicked(self):
        from Login import Login  
        self.login_window = tk.Toplevel(self.root)
        login = Login(self.login_window)
        self.root.withdraw()
        self.login_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

#Funcion para agregar el usuario a la base de datos
    def agregar_usuario(self):
            user = self.user_entry.get()
            password = self.password_entry.get()
            correo = self.correo_entry.get()

            if len(user) != 0 and len(password) != 0 and len(correo):
                conn = sqlite3.connect('user.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username=?", (user,))
                usuario_existente = cursor.fetchone()
                if usuario_existente:
                    conn.close()
                    return tkinter.messagebox.showerror(title="error", message="El usuario ingresado ya existe.")
                else:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (user, password))
                    conn.commit()
                    conn.close()
                    return tkinter.messagebox.showinfo(title="Registro exitoso.", message="Usuario registrado con exito.")
            else:
                return tkinter.messagebox.showerror(title="error", message="No has ingresado nada en los campos.")

    

def main():
    root = tk.Tk()
    register = Register(root)
    root.mainloop()

if __name__ == "__main__":
    main()
