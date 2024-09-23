import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os




# Diccionario de categorías y extensiones
file_types = {
    'Documentos': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'],
    'Imágenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'Música': ['.mp3', '.wav', '.flac'],
    'Archivos comprimidos': ['.zip', '.rar', '.tar', '.gz'],
    'Ejecutables': ['.exe', '.msi', '.dmg'],
    'Scripts': ['.py'],
    'Otros': []
}

#Seleciones

checkboxes = {}

#Crea carpetas si no existe
def create_folder(folder_name,direccionAOrganizar):
    folder_path = os.path.join(direccionAOrganizar, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Mueve el archivo a la carpte 
def move_file(file_name, folder_name,direccionAOrganizar):
    source = os.path.join(direccionAOrganizar, file_name)
    destination = os.path.join(create_folder(folder_name,direccionAOrganizar), file_name)
    shutil.move(source, destination)

# Organiza el archivo
def organize_archivos(direccionAOrganizar):
    for file_name in os.listdir(direccionAOrganizar):
        
        # Ignora carpetas
        if os.path.isdir(os.path.join(direccionAOrganizar, file_name)):
            continue
        
        # Obtener la extensión del archivo
        _, extension = os.path.splitext(file_name)
        file_moved = False

        # Clasificar el archivo según su extensión
        
        for folder_name, var in checkboxes.items():
            if var.get():
                extensions = file_types[folder_name]
                if extension.lower() in extensions:
                    move_file(file_name, folder_name,direccionAOrganizar)
                    file_moved = True
                    break
        
        # Si no coincide con ninguna categoría, mover a 'Otros'
        if checkboxes['Otros'].get() and not file_moved:
            move_file(file_name, 'Otros',direccionAOrganizar)
            
            
#____________________________________________________________________________________________________________________________________________________#            
                                                            #Window
#____________________________________________________________________________________________________________________________________________________#         

# Función para cargar configuraciones desde un archivo
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
    return {"included_folders": [], "selected_types": []}

# Función para guardar configuraciones en un archivo
def save_config():
    config = {
        "included_folders": included_folders,
        "selected_types": selected_types
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)


# Confirmar selección de tipos de archivos
def confirm_selection(window):
    global selected_types
    selected_types = [name for name, var in checkboxes.items() if var.get()]
    print (checkboxes)
    window.destroy()

# Función para abrir la ventana de selección de tipos de archivos
def open_selection_window():
    selection_window = tk.Toplevel(root)
    selection_window.title("Seleccionar Tipos de Archivos")

    # Crear una lista de tipos de archivos
    for foldername in file_types:
        var = tk.BooleanVar(value=(foldername in selected_types))
        print(foldername)
        checkbox = tk.Checkbutton(selection_window, text=foldername, variable=var)
        checkbox.pack(anchor='w')
        checkboxes[foldername] = var
    # Botón para confirmar selección
    confirm_button = tk.Button(selection_window, text="Aceptar", command=lambda: confirm_selection(selection_window))
    confirm_button.pack(pady=10)

# Agregar carpeta a la lista de inclusión
def add_included_folder():
    folder = filedialog.askdirectory()
    if folder and folder not in included_folders:
        included_folders.append(folder)
        update_included_listbox()

# Eliminar carpeta de la lista de inclusión
def remove_included_folder():
    selected = included_listbox.curselection()
    if selected:
        folder = included_listbox.get(selected)
        included_folders.remove(folder)
        update_included_listbox()

# Actualizar la lista de carpetas incluidas
def update_included_listbox():
    included_listbox.delete(0, tk.END)
    for folder in included_folders:
        included_listbox.insert(tk.END, folder)

# Función para organizar archivos
def organize():
    for folder in included_folders:
        print(f"Organizando archivos en: {folder}")
        organize_archivos(folder)


# Cargar configuraciones al iniciar
config = load_config()
included_folders = config.get("included_folders", [])
selected_types = config.get("selected_types", [])

root = tk.Tk()
root.title("Organizador de Archivos")

root.configure(bg='#001f3f')


# Botones para agregar y quitar carpetas
add_button = tk.Button(root, text="Agregar Carpeta a Incluir", bg="#124b85", fg="white",width=20, height=2, command=add_included_folder)
add_button.pack(pady=5)

remove_button = tk.Button(root, text="Eliminar Carpeta de Incluir",bg="#662929", fg="white", command=remove_included_folder)
remove_button.pack(pady=5)

select_types_button = tk.Button(root, text="Seleccionar Tipos de Archivos",bg="#124b85", fg="white", command=open_selection_window)
select_types_button.pack(pady=5)

# Listbox para mostrar carpetas incluidas
included_listbox = tk.Listbox(root, width=50, height=10,bg="#124b85", fg="white")
included_listbox.pack(pady=10)

# Botón para organizar archivos
organize_button = tk.Button(root, text="Organizar Archivos",bg="#124b85", fg="white", height=2, command=organize)
organize_button.pack(pady=10, fill='x')

# Actualizar lista al iniciar
update_included_listbox()

# Cerrar la aplicación guardando configuraciones
root.protocol("WM_DELETE_WINDOW", lambda: [save_config(), root.destroy()])
root.mainloop()

