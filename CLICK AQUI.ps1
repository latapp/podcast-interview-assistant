.\.venv\Scripts\Activate.ps1

Add-Type -AssemblyName System.Windows.Forms

$FileDialog = New-Object System.Windows.Forms.OpenFileDialog
$FileDialog.Title = "Selecciona un archivo"
$FileDialog.Filter = "Archivos Multimedia(*.mp3, *.mp4)|*.mp3;*.mp4"

if ($FileDialog.ShowDialog() -eq "OK") {
    $FilePath = $FileDialog.FileName
    Write-Host "Archivo seleccionado: $FilePath"

    # Ejecutar el script de Python pasando la ruta del archivo como argumento
    python main.py "$FilePath"
} else {
    Write-Host "No se seleccionó ningún archivo."
}