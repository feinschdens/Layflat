import tkinter as tk
from tkinter import simpledialog
import xml.etree.ElementTree as ET
import os

def indent(elem, level=0):
    """
    indent _summary_

    Args:
        elem (_type_): _description_
        level (int, optional): _description_. Defaults to 0.
    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def save_to_xml(data):
    """test

    Args:
        data (_type_): _description_
    """
    file_name = "data.xml"
    if os.path.exists(file_name):
        print("Datei existiert. Lese vorhandene Daten...")
        tree = ET.parse(file_name)
        root = tree.getroot()
    else:
        print("Erstelle neue Datei...")
        root = ET.Element("Data")
        tree = ET.ElementTree(root)

    for key, value in data.items():
        print(f"Füge Element hinzu: Schlüssel = {key}, Wert = {value}")
        ET.SubElement(root, "Pair", key=key).text = str(value)

    indent(root)
    print("Speichere Änderungen in 'data.xml'...")
    tree.write(file_name)
    print("Daten erfolgreich gespeichert!")

def ask_user_input():
    """test

    """
    data = {}
    root = tk.Tk()
    root.withdraw()  # Verbergen des Hauptfensters
    print("Benutzeroberfläche vorbereitet. Warte auf Benutzereingaben...")
    while True:
        key = simpledialog.askstring("Input", "Schlüssel eingeben (Leer lassen zum Beenden):", parent=root)
        if not key:
            print("Kein Schlüssel eingegeben. Beende die Eingabe...")
            break
        value = simpledialog.askstring("Input", f"Wert für {key} eingeben:", parent=root)
        data[key] = value
        print(f"Empfangen: Schlüssel = {key}, Wert = {value}")

    save_to_xml(data)
    root.mainloop()
    print("Benutzeroberfläche geschlossen.")

def new_func():
    """test#
    """

# Start der Anwendung
ask_user_input()
