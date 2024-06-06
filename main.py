import customtkinter
import tkinter
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os
import matplotlib.colors as mcolors
import random

"""
csv form:
    date,youtube,instagram,workout,study,read
    jj-mm-yyyy,xxx,xxx,...
"""

def read_file(filepath):
    file = open(filepath, "r")
    content = file.readlines()
    word = ""
    for i in range(len(content[0])):
        if(content[0][i] == ','):
            data_list.append([word])
            word = ""
            i+=1
        elif (content[0][i] == '\n'):
            data_list.append([word])
            i+=1
        else:
            word += content[0][i]
    content.pop(0)
    for i in range(len(content)):
        data = ""
        count = 0
        for j in range(len(content[i])):
            if(content[i][j] == ','):
                data_list[count].append(data)
                data = ""
                count += 1
                j+=1
            elif (content[i][j] == '\n'):
                data_list[count].append(data)
                count += 1
                j+=1
            else:
                data += content[i][j]

    # Adding color at the end of sub-lists
    colors = list(mcolors.CSS4_COLORS.keys())
    for i in range (1, len(data_list)):
        data_list[i].append(random.choice(colors))
    file.close()

def build_activity_graph(data):
    bgcolor = "#242424"
    textcolor='white'

    fig, ax = plt.subplots()
    fig.set_facecolor(bgcolor)
    ax.set_facecolor(bgcolor)

    for i in range (1,len(data)):
        data_name = data[i][0]
        plt.plot(data[0][1:], data[i][1:-1], color=data_list[i][-1], linestyle='dashed', marker='o', label=data_name)

    ax.set_ylabel("Time(min)", color=textcolor)
    ax.set_xlabel('Dates', color=textcolor)
    ax.set_title('Activity Report', fontsize=20, color=textcolor)
    ax.tick_params(axis='x', colors=textcolor)
    ax.tick_params(axis='y', colors=textcolor)

    # Définir la couleur de la légende
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color(textcolor)

    ax.grid()
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig('activity_report.png')
    
def on_resize(event):
    exit_button.place(x=event.width - 20 - exit_button.winfo_width(),
                      y=event.height - 20 - exit_button.winfo_height())

def user_input():
    # Créer une nouvelle fenêtre
    input_window = customtkinter.CTkToplevel(app)
    input_window.title("Add an Entry")
    input_window.geometry("300x400")

    def submit():
        activity = activity_var.get()
        unit = unit_var.get()
        value = value_entry.get()
        if unit == "hours":
            value = float(value) * 60  # Convertir en minutes
        print(f"Activity: {activity}, Value: {value} minutes")
        input_window.destroy()

    activity_options = [item[0] for item in data_list]

    # Variable pour l'activité
    activity_var = customtkinter.StringVar(value="youtube")
    activity_label = customtkinter.CTkLabel(input_window, text="Select Activity:")
    activity_label.pack(pady=5)
    activity_option_menu = customtkinter.CTkOptionMenu(input_window, variable=activity_var, values=activity_options)
    activity_option_menu.pack(pady=5)

    # Variable pour l'unité
    unit_var = customtkinter.StringVar(value="minutes")
    unit_label = customtkinter.CTkLabel(input_window, text="Select Unit:")
    unit_label.pack(pady=5)
    unit_option_menu = customtkinter.CTkOptionMenu(input_window, variable=unit_var, values=["minutes", "hours"])
    unit_option_menu.pack(pady=5)

    # Champ de saisie pour la valeur
    value_label = customtkinter.CTkLabel(input_window, text="Enter Value:")
    value_label.pack(pady=5)
    value_entry = customtkinter.CTkEntry(input_window)
    value_entry.pack(pady=5)

    # Bouton de soumission
    submit_button = customtkinter.CTkButton(input_window, text="Submit", command=submit)
    submit_button.pack(pady=10)

# Generate activity report
data_list = []
read_file('data.txt')
build_activity_graph(data_list)

# Creating GUI
app = customtkinter.CTk()
app.geometry("1600x970")

# Creating widgets for GUI
exit_button = customtkinter.CTkButton(app, text="Exit", command=app.destroy, fg_color="blue", corner_radius=25)
exit_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor='se')

activity_report_img = customtkinter.CTkImage(light_image=Image.open('activity_report.png'),
	dark_image=Image.open('activity_report.png'),
	size=(650,450))
label_for_image = customtkinter.CTkLabel(app, text="", image=activity_report_img)
label_for_image.place(relx=0.5, rely=0.30, anchor='c')

input_button = customtkinter.CTkButton(app, text="Add an entry", command=user_input, fg_color="blue", corner_radius=25)
input_button.place(relx=1.0, rely=1.0, x=-20 - exit_button.winfo_reqwidth() - 20, y=-20, anchor='se')
# Execute GUI
app.bind('<Configure>', on_resize)
app.mainloop()
