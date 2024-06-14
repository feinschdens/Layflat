import os

arial_path = 'C:/Windows/Fonts/arial.ttf'

if os.path.exists(arial_path):
    print(f"Arial-Schriftart gefunden unter: {arial_path}")
else:
    print("Arial-Schriftart nicht gefunden. Überprüfen Sie den Pfad.")
