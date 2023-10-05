import tkinter as tk                          # agregado para gui
import sys                                    # agregado llamada al sistema
from DatabaseManager import DatabaseManager   # agregado modificar valores de la base de datos
from Register import Register
from tkinter.font import BOLD
import tkinter.messagebox
class Login:
# funcion de la GUI
    def __init__(self, root):
        self.db_manager = DatabaseManager()
        self.root = root
        root.geometry('350x500+800+200')
        root.title('NetScanner')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(width=0, height=0)

        #frame_form
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form

         #frame_form_top
        frame_form_top = tk.Frame(frame_form,height = 40, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de Sesion",font=('Times', 30), fg="white",bg='#0D7FD8',pady=45)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        #end frame_form_top

        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        user_label = tk.Label(frame_form_fill, text="Usuario:", font=('Times', 14) ,fg="black",bg='#fcfcfc', anchor="w")
        user_label.pack(fill=tk.X, padx=20,pady=5)

        self.username_entry = tk.Entry(frame_form_fill, font=('Times', 16))
        self.username_entry.pack(fill=tk.X, padx=20,pady=5)

        password_label = tk.Label(frame_form_fill, text="Contraseña:", font=('Times', 16),fg="black",bg='#fcfcfc' , anchor="w")
        password_label.pack(fill=tk.X, padx=20,pady=5)

        self.password_entry = tk.Entry(frame_form_fill, font=('Times', 14))
        self.password_entry.pack(fill=tk.X, padx=20,pady=5)
        self.password_entry.config(show="*")

        login = tk.Button(frame_form_fill,text="Iniciar sesion",font=('Times', 15,BOLD),bg='#D8300D', bd=2,fg="#fff",command=self.authenticate_user)
        login.pack(fill=tk.X, padx=20,pady=10)

        register = tk.Button(frame_form_fill,text="Registrase",font=('Times', 15,BOLD),bg='#fff', bd=2,fg="#0D7FD8",command=self.open_register)
        register.pack(fill=tk.X, padx=20,pady=5)

        cerrar = tk.Button(frame_form_fill,text="Cerrar",font=('Times', 15,BOLD),bg='#0D7FD8', bd=2,fg="#fff",command=self.exit_program)
        cerrar.pack(fill=tk.X, padx=20,pady=5)

        self.root.bind("<Return>", lambda event: self.authenticate_user())
        self.root.bind("<Escape>", lambda event: self.exit_program())


# funcion para validar usuario en la base de datos
    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if self.db_manager.authenticate_user(username,password):
                self.authenticated_username = username
                self.open_dashboard() 
            else:
                return tkinter.messagebox.showerror(title="error",message="El usuario o contraseña es incorrecto.")
        else:
            return tkinter.messagebox.showerror(title="error", message="No has ingresado nada en los campos.")


    
# funcion para el boton de cerrar
    def exit_program(self):
        self.root.destroy()
        if hasattr(self, 'dash_window'):
            self.dash_window.destroy()
        sys.exit(0)


# funcion para crear la ventana del llamado dashboard
    def open_dashboard(self):
        from Dashboard import Dashboard  
        self.dash_window = tk.Toplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.exit_program)
        dash = Dashboard(self.dash_window,self.authenticated_username)

    #funcion para crear ventana de registro de usuario
    def open_register(self):
        from Register import Register
        self.dash_window = tk.Toplevel(self.root)
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.exit_program)
        register = Register(self.dash_window)
        
# funcion para la ventana principal de login
def main():
    root = tk.Tk()
    login = Login(root)
    root.mainloop()

if __name__ == "__main__":
    main()




