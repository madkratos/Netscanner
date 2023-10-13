import customtkinter                          # agregado para la gui moderna
import tkinter as tk                          # agregado para gui
from tkinter import filedialog                # agregado para cargar/guardar texto
from Register import Register                 # agregado para centrar la ventana
from DatabaseManager import DatabaseManager   # agregado modificar valores de la base de datos
from CTkMessagebox import CTkMessagebox       # agregado para mensajes de confirmación 
from tkinter import messagebox, ttk           # agregado para la table de datos treeview
class Tasks:
# funcion para la GUI
    def __init__(self, root,authenticated_username):
        self.db_manager = DatabaseManager()
        self.db_manager.create_task_tables()
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.geometry('350x500+800+200')
        root.title('NetScanner')
        self.root.resizable(width=0, height=0)


        self.frame = customtkinter.CTkFrame(master=root,width=330,height=70,corner_radius=10)
        self.frame.place(x=10, y=10)

        self.title_label =customtkinter.CTkLabel(master=self.frame, text="Gestor de Tareas", font=customtkinter.CTkFont(size=30),padx=50,pady=5)
        self.title_label.place(x=1, y=4)

        self.task_name_label = customtkinter.CTkLabel(master=root,text="Tarea:",font=customtkinter.CTkFont(size=15))
        self.task_name_label.place(x=20, y=95)

        self.task_name_entry = customtkinter.CTkEntry(master=root,width=100,height=20,corner_radius=8)
        self.task_name_entry.place(x=65, y=100)

        self.state_label = customtkinter.CTkLabel(self.root, text="Estado:",font=customtkinter.CTkFont(size=15))
        self.state_label.place(x=175, y=95)
        self.state_values = ["Nuevo", "En proceso", "Completado"]
        self.state_list = customtkinter.CTkComboBox(self.root, values=self.state_values,width=100,height=20,corner_radius=8)
        self.state_list.place(x=230, y=100)

        self.description_label = customtkinter.CTkLabel(master=root,text="Descripcion:",font=customtkinter.CTkFont(size=15))
        self.description_label.place(x=30, y=130)

        self.description_entry = customtkinter.CTkScrollableFrame(master=root, width=200, height=6)
        self.description_entry.place(x=120, y=130)
        self.text = tk.Text(master=self.description_entry, height=7, width=30,bg="#3B3B3B",fg="white")
        self.text.pack()
        
        self.save_button = customtkinter.CTkButton(master =root, text="Agregar",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.save_task)
        self.save_button.place(x=70, y=180, anchor=customtkinter.CENTER)

        self.delete_button = customtkinter.CTkButton(master =root, text="Borrar",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.delete_task_wrapper)
        self.delete_button.place(x=80, y=370, anchor=customtkinter.CENTER)

        self.read_button = customtkinter.CTkButton(master =root, text="Leer/edit",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.edit_task)
        self.read_button.place(x=75, y=340, anchor=customtkinter.CENTER)

        self.description_button = customtkinter.CTkButton(master =root, text="Ver Detalle",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.show_description)
        self.description_button.place(x=70, y=310, anchor=customtkinter.CENTER)

        self.back_button = customtkinter.CTkButton(master =root, text="Atras",fg_color="#3D59AB",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.back_button_clicked)
        self.back_button.place(x=315, y=65, anchor=customtkinter.CENTER)


        self.treeview_frame = customtkinter.CTkScrollableFrame(master=root, width=200, height=200)
        self.treeview_frame.place(x=120, y=260)

        self.task_list_treeview = ttk.Treeview(self.treeview_frame, columns=("Title", "State"))
        self.task_list_treeview.place(x=10, y=250)

        self.task_list_treeview.heading("Title", text="Tarea")
        self.task_list_treeview.heading("State", text="Estado")
      
        self.task_list_treeview.column("#0", width=0, minwidth=0)
        self.task_list_treeview.column("Title", width=100)
        self.task_list_treeview.column("State", width=100)
        self.task_list_treeview.pack()
        self.display_task()
        self.selected_task = None
        

# funcion para mostrar las tareas
    def display_task(self):
        self.task_list_treeview.delete(*self.task_list_treeview.get_children())
        tasks = self.db_manager.get_task()
        if tasks:
            for task in tasks:
                task_title = task["title"]
                task_state = task["state"]
                task_description = task["description"]
                self.task_list_treeview.insert("", "end", values=(task_title, task_state, task_description))
  
  

# funcion para el boton que lee la descripcion de la tarea
    def show_description(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            description = self.task_list_treeview.item(selected_item, "values")[2]
            CTkMessagebox(title="Detalle", message=description)


# funcion para actualizar las tareas
    def refresh(self):
        self.text.delete("1.0", tk.END)
        self.display_task()


#funcion para el boton de editar
    def edit_task(self):
        if self.selected_task is None:
            selected_item = self.task_list_treeview.selection()
            if selected_item:
                self.selected_task = selected_item
                self.read_button.configure(text="Guardar")
                title = self.task_list_treeview.item(selected_item, "values")[0]
                state = self.state_list.get()
                description = self.task_list_treeview.item(selected_item, "values")[2]
                self.task_name_entry.delete(0, tk.END)
                self.task_name_entry.insert(0, title)
                self.state_list.set(state)
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", description)
        else:
            new_title = self.task_name_entry.get()
            new_state = self.state_list.get()
            new_description = self.text.get("1.0", tk.END)
            if new_title and new_state:
                option = CTkMessagebox(title='Confirme la operación', message='¿Está seguro de querer editar esta tarea?', icon="question", option_2="Si", option_1="No")
                option = option.get()
                if option == "Si":
                    if self.db_manager.title_exists(new_title):
                        self.db_manager.update_task(new_title, new_state, new_description)
                        CTkMessagebox(message="Tarea editada con éxito", icon="check", option_1="Aceptar")
                        self.refresh()
                        self.reset_task_fields()
                    else:
                        CTkMessagebox(title="Operacion no valida", message="La tarea no existe", icon="warning", option_1="Aceptar")
                else:
                    CTkMessagebox(title="Operacion cancelada", message="Tarea no fue creada.")
            else:
                CTkMessagebox(title="Operacion no valida", message="Debe seleccionar el nombre de la tarea", icon="warning", option_1="Aceptar")


    def reset_task_fields(self):
            self.task_name_entry.delete(0, tk.END)
            self.state_list.set("")  
            self.text.delete("1.0", tk.END)
            self.selected_task = None
            self.read_button.configure(text="Leer/edit") 

# funcion para el boton de crear tarea
    def save_task(self):
        title = self.task_name_entry.get()
        state = self.state_list.get()
        description = self.text.get("1.0", tk.END)
        if title and state:
            option= CTkMessagebox(title='Confirme la operacion', message='Esta seguro de querer crear esta tarea?',icon="question",option_2="Si", option_1="No") 
            option = option.get()
            if option =="Si":
                self.db_manager.insert_task(title, state, description)
                self.refresh()
                CTkMessagebox(message=f"La tarea {title} se creo con exito",icon="check", option_1="Aceptar")
                self.task_name_entry.delete(0, tk.END)
                self.text.delete("1.0", tk.END)
                self.task_name_entry.focus()
                
            else:
                CTkMessagebox(title="Operacion cancelada", message="Tarea no fue creada.")
                self.task_name_entry.delete(0, tk.END)
                self.text.delete("1.0", tk.END)
                self.task_name_entry.focus()
        else:
            CTkMessagebox(title="Operacion no valida", message="Por favor, complete los campos",icon="warning", option_1="Acptar")


# funcion para borrar la tarea
    def delete_task(self, title):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            title = self.task_list_treeview.item(selected_item, "values")[0]
            if title:
                if self.db_manager.title_exists(title):
                    option = CTkMessagebox(title='Confirme la operación', message='¿Está seguro de querer eliminar esta tarea?', icon="question", option_2="Sí", option_1="No")
                    option = option.get()
                    if option == "Sí":
                        self.db_manager.delete_task(title)
                        self.refresh()
                        CTkMessagebox(message="Tarea borrada con éxito", icon="check", option_1="Aceptar")
                    else:
                        CTkMessagebox(title="Operación cancelada.", message="Tarea no eliminada.")
                else:
                    CTkMessagebox(title="Operacion no valida", message="La tarea no existe",icon="warning", option_1="Acptar")
            else:
                CTkMessagebox(title="Operacion no valida", message="Debe seleccionar el nombre de la tarea",icon="warning", option_1="Acptar")
        else:
            CTkMessagebox(title="Operacion no valida", message="No ha seleccionado una tarea para borrar",icon="warning", option_1="Acptar")


# funcion para el boton de borrar la tarea 
    def delete_task_wrapper(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            title = self.task_list_treeview.item(selected_item, "values")[0]
            self.delete_task(title)
        else:
            CTkMessagebox(title="Operacion no valida", message="No ha seleccionado una tarea para borrar", icon="warning", option_1="Acptar")

# funcion para restaurar la ventana 
    def restore_dashboard(self):
        self.dash_window.destroy()

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

# funcion que da inicio al loop de la GUI 
def main():
    root = customtkinter.CTk()
    task = Tasks(root)
    root.mainloop()

if __name__ == "__main__":
    main()


