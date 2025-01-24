""" import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re
import xml.etree.ElementTree as ET

def generate_mod107_xml(input_csv_path, output_xml_path):
    try:
        # Load the tabular data from a CSV file
        data = pd.read_csv(input_csv_path,delimiter="\t",encoding="ISO-8859-1")
        def clean_column_names(columns):
            return [re.sub(r'[^\w]', '_', col).lower() for col in columns]

        data.columns = clean_column_names(data.columns)
        print("Cleaned column names:", data.columns.tolist())

        # Initialize the XML root element
        root = ET.Element("mod107")

        # Add main attributes for Modelo 107
        tp_dec = ET.SubElement(root, "tp_dec")
        tp_dec.text = "1"  # Assuming it's within the reporting deadline

        livros = ET.SubElement(root, "livros", vendas="1", compras="0")

        periodo = ET.SubElement(root, "periodo", ano="2024", tri="2")

        cd_af = ET.SubElement(root, "cd_af")
        cd_af.text = "123"  # Example fiscal area code

        nif = ET.SubElement(root, "nif")
        nif.text = "987654321"  # Example taxpayer NIF

        nome = ET.SubElement(root, "nome")
        nome.text = "Cantinho C"  # Example taxpayer name

        # Add the sales book (Livro de Vendas)
        vendas = ET.SubElement(root, "vendas")
        linhas = ET.SubElement(vendas, "linhas")
        
        data["montante"] = data["montante"].str.replace(",", ".").astype(float)

        # Populate XML with rows from the table
        for _, row in data.iterrows():
            linha = ET.SubElement(linhas, "linha", {
                "origem": "CV",  # Assuming Cabo Verde as the origin
                "nif": str(row["entidade"]),
                "designacao": row["nome_da_entidade"],
                "tp_doc": "FT",  # Assuming "FT" (Fatura) as the document type
                "serie": row["doc__origem"].split('.')[0],  # Series from document reference
                "num_doc": row["doc__origem"].split('.')[-1],  # Document number
                "data": row["data_de_lan_amento"].split(' ')[0],  # Extract date
                "vl_base_incid": str(row["montante"]),
                "taxa": "4",  # Assuming a 4% tax rate
                "imp": str(float(row["montante"]) * 0.04),  # Calculate tax
                "tipologia": "SRV",  # Assuming services
                "tp_oper": "N"  # Normal operation
            })

        # Calculate totals
        total_base = data["montante"].astype(float).sum()
        total_tax = total_base * 0.04

        # Add totals for the sales book
        totais = ET.SubElement(vendas, "totais", {
            "vl_base_incid": str(total_base),
            "imp": str(total_tax)
        })

        # Convert the XML tree to a string
        xml_string = ET.tostring(root, encoding="utf-8", method="xml")

        # Save the XML to a file
        with open(output_xml_path, "wb") as xml_file:
            xml_file.write(xml_string)

        messagebox.showinfo("Success", f"XML file successfully generated:\n{output_xml_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def browse_input_file():
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(
        title="Save XML File",
        defaultextension=".xml",
        filetypes=(("XML Files", "*.xml"), ("All Files", "*.*"))
    )
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def generate_xml():
    input_csv_path = input_file_entry.get()
    output_xml_path = output_file_entry.get()

    if not input_csv_path or not output_xml_path:
        messagebox.showwarning("Warning", "Please select both input and output files!")
        return

    generate_mod107_xml(input_csv_path, output_xml_path)

# Create the GUI application
root = tk.Tk()
root.title("Modelo 107 XML Generator")

# Input file selection
tk.Label(root, text="Select Input CSV File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)
browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=10, pady=5)

# Output file selection
tk.Label(root, text="Select Output XML File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)
browse_output_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_output_button.grid(row=1, column=2, padx=10, pady=5)

# Generate button
generate_button = tk.Button(root, text="Generate XML", command=generate_xml, bg="green", fg="white")
generate_button.grid(row=2, column=1, padx=10, pady=10)

# Start the GUI application
root.mainloop() """


import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re
import xml.etree.ElementTree as ET

def generate_mod107_xml(input_csv_path, output_xml_path):
    try:
        # Load the tabular data from a CSV file
        data = pd.read_csv(input_csv_path, delimiter="\t", encoding="ISO-8859-1")
        
        # Clean column names
        def clean_column_names(columns):
            return [re.sub(r'[^\w]', '_', col).lower() for col in columns]

        data.columns = clean_column_names(data.columns)

        # Separate sales and purchase data
        sales_data = data[data["conta"].astype(str).str.startswith("7")]  # Assuming '7' prefix is for sales accounts
        purchase_data = data[data["conta"].astype(str).str.startswith("6")]  # Assuming '6' prefix is for purchases

        # Initialize the XML root element
        root = ET.Element("mod107")

        # Add main attributes for Modelo 107
        tp_dec = ET.SubElement(root, "tp_dec")
        tp_dec.text = "1"  # Assuming it's within the reporting deadline

        livros = ET.SubElement(root, "livros", vendas="1", compras="1")

        periodo = ET.SubElement(root, "periodo", ano="2024", tri="2")

        cd_af = ET.SubElement(root, "cd_af")
        cd_af.text = "123"  # Example fiscal area code

        nif = ET.SubElement(root, "nif")
        nif.text = "987654321"  # Example taxpayer NIF

        nome = ET.SubElement(root, "nome")
        nome.text = "Cantinho C"  # Example taxpayer name

        # Add the sales book (Livro de Vendas)
        vendas = ET.SubElement(root, "vendas")
        linhas_vendas = ET.SubElement(vendas, "linhas")
        
        # Ensure Montante is properly converted
        sales_data["montante"] = sales_data["montante"].str.replace(",", ".").astype(float)

        for _, row in sales_data.iterrows():
            linha = ET.SubElement(linhas_vendas, "linha", {
               "origem": "CV",  # Assuming Cabo Verde as the origin
                "nif": str(row["entidade"]),
                "designacao": row["nome_da_entidade"],
                "tp_doc": "FT",  # Assuming "FT" (Fatura) as the document type
                "serie": row["doc__origem"].split('.')[0],  # Series from document reference
                "num_doc": row["doc__origem"].split('.')[-1],  # Document number
                "data": row["data_de_lan_amento"].split(' ')[0],  # Extract date
                "vl_base_incid": str(row["montante"]),
                "taxa": "4",  # Assuming a 4% tax rate
                "imp": str(float(row["montante"]) * 0.04),  # Calculate tax
                "tipologia": "SRV",  # Assuming services
                "tp_oper": "N"  # Normal operation
            })

        # Add totals for sales
        total_sales_base = sales_data["montante"].sum()
        total_sales_tax = total_sales_base * 0.04
        ET.SubElement(vendas, "totais", {
            "vl_base_incid": str(total_sales_base),
            "imp": str(total_sales_tax)
        })

        # Add the purchase book (Livro de Compras)
        compras = ET.SubElement(root, "compras")
        linhas_compras = ET.SubElement(compras, "linhas")

        # Ensure Montante is properly converted for purchases
        purchase_data["montante"] = purchase_data["montante"].str.replace(",", ".").astype(float)

        for _, row in purchase_data.iterrows():
            linha = ET.SubElement(linhas_compras, "linha", {
                "origem": "CV",  # Assuming Cabo Verde as the origin
                "nif": str(row["entidade"]),
                "designacao": row["nome_da_entidade"],
                "tp_doc": "FT",
                "serie": row["doc__origem"].split('.')[0],
                "num_doc": row["doc__origem"].split('.')[-1],
                "data": row["data_de_lan_amento"].split(' ')[0],
                "vl_base_incid": str(row["montante"]),
                "taxa": "15",  # Assuming a 15% tax rate for purchases
                "imp": str(float(row["montante"]) * 0.15),
                "tipologia": "OBC",
                "tp_oper": "N"

            })

        # Add totals for purchases
        total_purchase_base = purchase_data["montante"].sum()
        total_purchase_tax = total_purchase_base * 0.15
        ET.SubElement(compras, "totais", {
            "vl_base_incid": str(total_purchase_base),
            "imp": str(total_purchase_tax)
        })

        # Convert the XML tree to a string
        xml_string = ET.tostring(root, encoding="utf-8", method="xml")

        # Save the XML to a file
        with open(output_xml_path, "wb") as xml_file:
            xml_file.write(xml_string)

        messagebox.showinfo("Success", f"XML file successfully generated:\n{output_xml_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def browse_input_file():
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(
        title="Save XML File",
        defaultextension=".xml",
        filetypes=(("XML Files", "*.xml"), ("All Files", "*.*"))
    )
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def generate_xml():
    input_csv_path = input_file_entry.get()
    output_xml_path = output_file_entry.get()

    if not input_csv_path or not output_xml_path:
        messagebox.showwarning("Warning", "Please select both input and output files!")
        return

    generate_mod107_xml(input_csv_path, output_xml_path)

# Create the GUI application
root = tk.Tk()
root.title("Modelo 107 XML Generator")

# Input file selection
tk.Label(root, text="Select Input CSV File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)
browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=10, pady=5)

# Output file selection
tk.Label(root, text="Select Output XML File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)
browse_output_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_output_button.grid(row=1, column=2, padx=10, pady=5)

# Generate button
generate_button = tk.Button(root, text="Generate XML", command=generate_xml, bg="green", fg="white")
generate_button.grid(row=2, column=1, padx=10, pady=10)

# Start the GUI application
root.mainloop()
