# Anzahl der Dateien pro Startziffer
$filesPerPrefix = 5

# Startziffern und Zielverzeichnis
$prefixes = @("4", "5", "2", "8")
$directoryPath = "C:\Users\peter\Documents\Scripts\sammler"

# Funktion, um zufällige Zahlen für die restlichen Teile des Dateinamens zu generieren
function Get-RandomPart {
    param (
        [int]$min,
        [int]$max
    )
    return Get-Random -Minimum $min -Maximum $max
}

# Array, um alle Dateinamen zu speichern
$dateinamen = @()

foreach ($prefix in $prefixes) {
    for ($i = 0; $i -lt $filesPerPrefix; $i++) {
        # Generieren der restlichen Teile des Dateinamens
        $part1 = Get-RandomPart -min 100 -max 999
        $part2 = Get-RandomPart -min 0 -max 9
        $part3 = Get-RandomPart -min 10 -max 99
        $part4 = Get-RandomPart -min 10000000000 -max 99999999999

        # Zusammenbauen des Dateinamens
        $dateiname = "$prefix-$part1-$part2-$part3-$part4.pdf"
        $dateinamen += $dateiname
    }
}

# Dateinamen ausgeben
$dateinamen | ForEach-Object { Write-Host $_ }
