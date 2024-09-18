import json
import pandas as pd
from tkinter import Tk, Button, Entry, Label, filedialog, messagebox, DoubleVar
from tkinter import ttk
import os
from threading import Thread
from translate import Translator
import tkinter as tk
import re

selected_files = []
destination_folder = ""
merged_file_path = ""
translated_file_path = ""

def merge_localization_files(file_paths, output_file, progress_callback):
    merged_data = {
        "$schema": "",
        "locale": "en-US",  # You can change this to the desired locale
        "localizedText": {}
    }
    total_files = len(file_paths)
    
    for i, file in enumerate(file_paths):
        try:
            print(f"Processing file: {file}")  # Debugging statement
            with open(file, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                if not content.strip():  # Check if content is empty
                    messagebox.showerror("Error", f"File {file} is empty.")
                    return
                
                try:
                    data = json.loads(content)
                except json.JSONDecodeError as e:
                    messagebox.showerror("Error", f"Failed to decode JSON in file {file}. Error: {str(e)}")
                    return
                
                if "localizedText" in data and isinstance(data["localizedText"], dict):
                    merged_data["localizedText"].update(data["localizedText"])
                else:
                    messagebox.showerror("Error", f"File {file} does not have a valid 'localizedText' section.")
                    return
            
            progress_callback(i + 1, total_files)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file {file}: {str(e)}")
            return

    # Use the last file's schema as the output schema
    merged_data["$schema"] = data.get("$schema", "")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            json.dump(merged_data, f_out, indent=4, ensure_ascii=False)
        messagebox.showinfo("Success", f"Merged localization data has been saved to {output_file}")
        global merged_file_path
        merged_file_path = output_file
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the merged file: {str(e)}")

def capitalize_text(text):
    if text:
        # Capitalize the first letter of each word in the text
        return ' '.join(word.capitalize() for word in text.split())
    return text

def preserve_case(original, translated):
    # Define terms to preserve in a case-insensitive manner
    terms_to_preserve = ['FE', 'TUTCO', 'GLT', 'MGT', 'LLT', 'EnBW']
    
    # Create a dictionary to preserve terms in the original case
    case_map = {term.lower(): term for term in terms_to_preserve}

    # Function to replace term with preserved case
    def replace_case_sensitive(match):
        term = match.group()
        return case_map.get(term.lower(), term)
    
    # Compile regex pattern to match terms in a case-insensitive manner
    pattern = re.compile(r'\b(' + '|'.join(re.escape(term) for term in terms_to_preserve) + r')\b', re.IGNORECASE)
    translated_corrected = pattern.sub(replace_case_sensitive, translated)
    
    return translated_corrected

def translate_merged_file():
    if not merged_file_path:
        messagebox.showerror("Error", "No merged file available. Please merge the files first.")
        return

    # Initialize the offline translator (e.g., using English to German translation)
    translator = Translator(from_lang='de', to_lang='en')

    try:
        with open(merged_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Preserve the structure of the original file, only translating the localizedText values
        translated_data = data.copy()
        if "localizedText" in data and isinstance(data["localizedText"], dict):
            translated_localized_text = {}
            total_keys = len(data["localizedText"])
            
            for i, (key, value) in enumerate(data["localizedText"].items()):
                if not isinstance(value, str) or value is None:
                    translated_localized_text[key] = value
                    continue

                try:
                    # Translate the value only
                    translated_value = translator.translate(value)
                    # Preserve the case for specific terms
                    translated_value = preserve_case(value, translated_value)
                    # Capitalize each word in the translated value
                    translated_value = capitalize_text(translated_value)
                except Exception as e:
                    translated_value = value  # Retain the original value in case of error
                
                translated_localized_text[key] = translated_value
                
                update_translation_progress(i + 1, total_keys)

            translated_data["localizedText"] = translated_localized_text
        else:
            messagebox.showerror("Error", "Unexpected data format in the merged file.")
            return

        global translated_file_path
        translated_file_path = os.path.join(destination_folder, "translated_" + os.path.basename(merged_file_path).replace('.json', '.localization'))
        with open(translated_file_path, 'w', encoding='utf-8') as f_out:
            json.dump(translated_data, f_out, indent=4, ensure_ascii=False)
        messagebox.showinfo("Success", f"Translated localization data has been saved to {translated_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to translate the file: {str(e)}")

def update_translation_progress(current, total):
    translation_progress_var.set((current / total) * 100)
    root.update_idletasks()

def select_localization_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(filetypes=[("Localization Files", "*.localization")])
    if selected_files:
        messagebox.showinfo("Files Selected", f"Selected {len(selected_files)} file(s)")

def select_destination_folder():
    global destination_folder
    destination_folder = filedialog.askdirectory()
    if destination_folder:
        messagebox.showinfo("Folder Selected", f"Selected folder: {destination_folder}")

def merge_files():
    if not selected_files:
        messagebox.showerror("Error", "No files selected. Please select localization files.")
        return

    if not destination_folder:
        messagebox.showerror("Error", "No destination folder selected. Please select a destination folder.")
        return

    filename = output_name.get()
    if not filename:
        messagebox.showerror("Error", "Please enter a name for the output file.")
        return
    if not filename.endswith('.localization'):
        filename += '.localization'
    
    full_output_path = os.path.join(destination_folder, filename)
    
    thread = Thread(target=merge_localization_files, args=(selected_files, full_output_path, lambda c, t: None))
    thread.start()

root = Tk()
root.title("TPDE: TwinCAT JSON Merger & Translator")
root.geometry("425x200")  

root.configure(bg="#2E2E2E")
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", background="#333333", foreground="orange", borderwidth=1)
style.configure("TLabel", background="#2E2E2E", foreground="orange")
style.configure("TProgressbar", background="#5E5E5E", troughcolor="#1E1E1E")

label = ttk.Label(root, text="Enter Output File Name:")
label.grid(row=0, column=0, padx=10, pady=10)

output_name = Entry(root, width=40, bg="#333333", fg="orange", insertbackground="orange")
output_name.grid(row=0, column=1, padx=10, pady=10)

merge_button = ttk.Button(root, text="Merge Files", command=merge_files)
merge_button.grid(row=2, column=0, padx=10, pady=10)

translate_button = ttk.Button(root, text="Translate Merged File", command=translate_merged_file)
translate_button.grid(row=2, column=1, padx=10, pady=10)

translation_progress_var = DoubleVar()
translation_progress_bar = ttk.Progressbar(root, variable=translation_progress_var, maximum=100)
translation_progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

select_files_button = ttk.Button(root, text="Select Files", command=select_localization_files)
select_files_button.grid(row=1, column=0, padx=10, pady=10)

select_folder_button = ttk.Button(root, text="Select Destination Folder", command=select_destination_folder)
select_folder_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
