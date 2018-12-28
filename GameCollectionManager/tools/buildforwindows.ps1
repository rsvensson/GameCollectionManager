$PythonEXE = "C:\Users\KRS\AppData\Local\Programs\Python\Python37\python.exe"
$GCMFile = "$PSScriptRoot\..\gcm.py"
$PyInstaller = "$PythonEXE -OO -m PyInstaller -F -w $GCMFile"
$SourceFolder = "C:\Users\KRS\Desktop\Game Collection Manager"
$DestinationFile = "$PSScriptRoot\..\Game Collection Manager.zip"
$Compression = "Optimal"

function Zip-Directory {
    Param(
        [Parameter(Mandatory=$True)][string]$DestinationFileName,
        [Parameter(Mandatory=$True)][string]$SourceDirectory,
        [Parameter(Mandatory=$False)][string]$CompressionLevel = "Optimal",
        [Parameter(Mandatory=$False)][switch]$IncludeParentDir
    )
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $CompressionLevel = [System.IO.Compression.CompressionLevel]::$CompressionLevel
    [System.IO.Compression.ZipFile]::CreateFromDirectory($SourceDirectory, $DestinationFileName, $CompressionLevel, $IncludeParentDir)
}

"Cleaning $SourceFolder"
Remove-Item $SourceFolder\* -recurse


"Removing old $DestinationFile"
Remove-Item $DestinationFile

"#########################"
"# Executing PyInstaller #"
"#########################"
iex $PyInstaller

"#####################"
"# Coping data files #"
"#####################"
New-Item -ItemType directory -Path "$SourceFolder\data\db"
Copy-Item -Path $PSScriptRoot\..\data\db\collection.db -Destination $SourceFolder\data\db
Copy-Item -Path $PSScriptRoot\..\data\vgdb -Destination $SourceFolder\data -Recurse
Copy-Item -Path $PSScriptRoot\..\dist\gcm.exe -Destination $SourceFolder

"Creating zip file $DestinationFile"
Zip-Directory -DestinationFileName $DestinationFile `
    -SourceDirectory $SourceFolder `
    -CompressionLevel $Compression `
    -IncludeParentDir