import os
import shutil

def sort_files_by_extension(directory):
    # Überprüfen, ob das Verzeichnis existiert
    if not os.path.exists(directory):
        print(f"Das Verzeichnis {directory} existiert nicht.")
        return

    # Durchlaufen aller Dateien im Verzeichnis
    for filename in os.listdir(directory):
        # Erstellen des vollständigen Pfads der Datei
        file_path = os.path.join(directory, filename)

        # Überprüfen, ob es sich um eine Datei handelt
        if os.path.isfile(file_path):
            # Extrahieren der Dateiendung
            file_extension = os.path.splitext(filename)[1][1:].lower()  # Dateiendung ohne Punkt und in Kleinbuchstaben

            # Überspringen von Dateien ohne Dateiendung
            if not file_extension:
                continue

            # Erstellen des Zielordners basierend auf der Dateiendung
            target_dir = os.path.join(directory, file_extension)

            # Erstellen des Zielordners, falls er nicht existiert
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # Verschieben der Datei in den Zielordner
            shutil.move(file_path, os.path.join(target_dir, filename))

    print("Dateien wurden erfolgreich sortiert.")

# Beispielnutzung
sort_files_by_extension("C:\\Users\\peter\\Pictures\\Familie\\Familie")
