import tkinter as tk
import customtkinter
from tkinter import filedialog
import camelot
import pandas as pd
import os


def table_extract(file_path, progressbar):
    tables = camelot.read_pdf(file_path, pages='all')
    table_data = []
    total_tables = len(tables)
    for i, table in enumerate(tables):
        table_frame = table.df
        data = pd.DataFrame(table_frame)
        data.to_excel(f'table_{i+1}.xlsx')
        table_data.append(data)
        progress = (i + 1) / total_tables * 100
        progressbar.set(progress)

    return table_data


def browse_pdf():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        # Display a message asking for confirmation
        success_label.config(
            text="Click 'Confirm Extraction' to extract tables")

        # Show the confirm button
        confirm_button.pack(padx=20, pady=10)
        progressbar.pack(padx=20, pady=10)
        progressbar.place(relx=0.5, rely=0.55, anchor='center')


def confirm_extraction():
    if file_path:
        extracted_tables = table_extract(file_path, progressbar)
        for i, data in enumerate(extracted_tables):
            print(f"Table {i+1}:")
            print(data.head())
        success_label.config(text="Tables extracted successfully")

        # Hide the progress bar after extraction is complete
        progressbar.pack_forget()


# Create a simple GUI for selecting a PDF file
root = customtkinter.CTk()
root.title("PDF Table Extractor")
root.iconbitmap('C:/Users/ASIS GUPTA /Desktop/Table extract but py/icon.ico')

# Load the background image
bg_image = tk.PhotoImage(file="backdrop.png")

# Create a Label widget for the background image
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)


label = tk.Label(root, text="Select a PDF file:", font=("Arial", 48))
label.place(relx=0.5, rely=0.5, anchor='center')

success_label = tk.Label(root, text="", font=("Arial", 18), fg="green")
success_label.place(relx=0.5, rely=0.6, anchor='center')

browse_button = customtkinter.CTkButton(
    root, text="Browse", command=browse_pdf)
browse_button.place(relx=0.5, rely=0.7, anchor='center')

# Create a frame to hold the confirm button (doesn't move)
confirm_frame = tk.Frame(root)
confirm_frame.place(relx=0.5, rely=0.8, anchor='center')

progressbar = customtkinter.CTkProgressBar(master=root)

# Create the confirm button inside the frame (hidden by default)
confirm_button = customtkinter.CTkButton(
    confirm_frame, text="Confirm Extraction", command=confirm_extraction)
confirm_button.pack()
confirm_button.pack_forget()  # Hide the confirm button initially

file_path = None  # Store the selected file path

root.mainloop()
