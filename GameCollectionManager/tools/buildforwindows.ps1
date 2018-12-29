$PythonEXE = where.exe python
$GCMFile = "$PSScriptRoot\..\gcm.py"
$BuildDir = "$PSScriptRoot\..\build"
$DistDir = "$PSScriptRoot\..\dist"
$PyInstaller = "$PythonEXE -OO -m PyInstaller -F -w --distpath $DistDir --workpath $BuildDir $GCMFile"
$SourceFolder = "$PSScriptRoot\..\output\Game Collection Manager"
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

if ($SourceFolder | Test-Path) {
    "Cleaning $SourceFolder"
    Remove-Item $SourceFolder\* -recurse
} else {
    New-Item -ItemType directory -Path $SourceFolder
}
if ($BuildDir | Test-Path) {
    "Cleaning old build directory"
    Remove-Item "$PSScriptRoot\..\build" -recurse
}
if ($DistDir | Test-Path) {
    "Cleaning old dist directory"
    Remove-Item "$PSScriptRoot\..\dist" -recurse
}
if ($DestinationFile | Test-Path) {
    "Removing old $DestinationFile"
    Remove-Item $DestinationFile
}

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
Copy-Item -Path $DistDir\gcm.exe -Destination $SourceFolder

"Creating zip file $DestinationFile"
Zip-Directory -DestinationFileName $DestinationFile `
    -SourceDirectory $SourceFolder `
    -CompressionLevel $Compression `
    -IncludeParentDir