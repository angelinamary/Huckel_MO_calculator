import re
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

def calculate_valence_electrons(file_path, atom_counts, charge):
    element_valence_electrons = {
        'H': 1,
        'He': 2,
        'Li': 1,
        'Be': 2,
        'B': 3,
        'C': 4,
        'N': 5,
        'O': 6,
        'F': 7,
        'Ne': 8,
        'Na': 1,
        'Mg': 2,
        'Al': 3,
        'Si': 4,
        'P': 5,
        'S': 6,
        'Cl': 7,
        'Ar': 8,
        'K': 1,
        'Ca': 2,
        'Sc': 3,
        'Ti': 4,
        'V': 5,
        'Cr': 6,
        'Mn': 7,
        'Fe': 8,
        'Co': 9,
        'Ni': 10,
        'Cu': 11,
        'Zn': 12,
        'Ga': 13,
        'Ge': 14,
        'As': 15,
        'Se': 16,
        'Br': 17,
        'Kr': 18,
        'Rb': 1,
        'Sr': 2,
        'Y': 3,
        'Zr': 4,
        'Nb': 5,
        'Mo': 6,
        'Tc': 7,
        'Ru': 8,
        'Rh': 9,
        'Pd': 10,
        'Ag': 11,
        'Cd': 12,
        'In': 13,
        'Sn': 14,
        'Sb': 15,
        'Te': 16,
        'I': 17,
        'Xe': 18,
        'Cs': 1,
        'Ba': 2,
        'La': 3,
        'Ce': 4,
        'Pr': 5,
        'Nd': 6,
        'Pm': 7,
        'Sm': 8,
        'Eu': 9,
        'Gd': 10,
        'Tb': 11,
        'Dy': 12,
        'Ho': 13,
        'Er': 14,
        'Tm': 15,
        'Yb': 16,
        'Lu': 17,
        'Hf': 4,
        'Ta': 5,
        'W': 6,
        'Re': 7,
        'Os': 8,
        'Ir': 9,
        'Pt': 10,
        'Au': 11,
        'Hg': 12,
        'Tl': 13,
        'Pb': 14,
        'Bi': 15,
        'Th': 4,
        'Pa': 5,
        'U': 6,
        'Np': 7,
        'Pu': 8,
        'Am': 9,
        'Cm': 10,
        'Bk': 11,
        'Cf': 12,
        'Es': 13,
        'Fm': 14,
        'Md': 15,
        'No': 16,
        'Lr': 17,
        'Rf': 4,
        'Db': 5,
        'Sg': 6,
        'Bh': 7,
        'Hs': 8,
        'Mt': 9,
        'Ds': 10,
        'Rg': 11,
        'Cn': 12,
        'Nh': 13,
        'Fl': 14,
        'Mc': 15,
        'Lv': 16,
        'Ts': 17,
        'Og': 18,
        'Fr': 1,
        'Ra': 2,
        'Ac': 3,
        'Th': 4,
        'Pa': 5,
        'U': 6,
        'Np': 7,
        'Pu': 8,
        'Am': 9,
        'Cm': 10,
        'Bk': 11,
        'Cf': 12,
        'Es': 13,
        'Fm': 14,
        'Md': 15,
        'No': 16,
        'Lr': 17,
        'Rf': 4,
        'Db': 5,
        'Sg': 6,
        'Bh': 7,
        'Hs': 8,
        'Mt': 9,
        'Ds': 10,
        'Rg': 11,
        'Cn': 12,
        'Nh': 13,
        'Fl': 14,
        'Mc': 15,
        'Lv': 16,
        'Ts': 17,
        'Og': 18,
    }

    total_electrons = 0
    results = []

    for element, count in atom_counts.items():
        valence_electrons = element_valence_electrons.get(element, 0)
        electrons = count * valence_electrons
        total_electrons += electrons
        electron_configuration = element_valence_electrons.get(element, "")
        results.append(f"{element} = {electron_configuration} = {valence_electrons} x {count} = {electrons}")

    huckel_electrons = total_electrons - charge
    homo = huckel_electrons // 2
    lumo = homo + 1

    results.append(f"\nTotal electrons = {total_electrons}")
    results.append(f"Total Huckel valence electrons of the complex considering its charge: {huckel_electrons}")
    results.append(f"HOMO: {homo}")
    results.append(f"LUMO: {lumo}")

    folder_path = os.path.dirname(file_path)
    with open(f"{folder_path}/results.txt", "w") as file:
        file.write("Valence configuration according to chemical formula:\n")
        for line in results:
            file.write(line + '\n')

    return results

def on_submit():
    file_path = xyz_entry.get()
    charge = int(charge_entry.get())

    if not file_path:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Please submit the XYZ file first.")
        return

    try:
        df = pd.read_csv(file_path, delimiter=r"\s+", header=None, skiprows=2)
        atom_counts = df[0].value_counts().to_dict()
    except Exception as e:
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Error reading the XYZ file: {e}")
        return

    results = calculate_valence_electrons(file_path, atom_counts, charge)

    output.delete("1.0", tk.END)
    for line in results:
        output.insert(tk.END, line + "\n")

def browse_xyz_file():
    file_path = filedialog.askopenfilename(filetypes=[("XYZ Files", "*.xyz")])
    xyz_entry.delete(0, tk.END)
    xyz_entry.insert(0, file_path)

root = tk.Tk()
root.title("Huckel Valence Electrons Calculator")

formula_label = tk.Label(root, text="Please submit the xyz file:")
formula_label.pack(pady=10)

xyz_entry = tk.Entry(root, width=50)
xyz_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_xyz_file)
browse_button.pack(pady=5)

charge_label = tk.Label(root, text="Please enter the overall charge of the complex:")
charge_label.pack(pady=5)

charge_entry = tk.Entry(root, width=10)
charge_entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

output = tk.Text(root, width=80, height=20, wrap=tk.WORD)
output.pack(pady=10)

root.mainloop()
