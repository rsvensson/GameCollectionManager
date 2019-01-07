$PythonEXE = where.exe python
$GCMFile = "$PSScriptRoot\..\gcm.py"
$BuildDir = "$PSScriptRoot\..\build"
$DistDir = "$PSScriptRoot\..\dist"
$PyInstaller = "$PythonEXE -OO -m PyInstaller -F -w --distpath $DistDir --workpath $BuildDir $GCMFile"
$SourceFolder = "$PSScriptRoot\..\output\Game Collection Manager"
$DestinationFile = "$PSScriptRoot\..\Game Collection Manager.7z"
set-alias 7z "$env:ProgramFiles\7-Zip\7z.exe"

if ($SourceFolder | Test-Path) {
    "Cleaning $SourceFolder"
    Remove-Item $SourceFolder\* -recurse
} else {
    New-Item -ItemType directory -Path $SourceFolder | Out-Null
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

""
"#########################"
"# Executing PyInstaller #"
"#########################"
""
iex $PyInstaller

""
"#####################"
"# Copying data files #"
"#####################"
""
New-Item -ItemType directory -Path "$SourceFolder\data\db"
Copy-Item -Path $PSScriptRoot\..\data\db\collection.db -Destination $SourceFolder\data\db
Copy-Item -Path $PSScriptRoot\..\data\vgdb -Destination $SourceFolder\data -Recurse
Copy-Item -Path $DistDir\gcm.exe -Destination $SourceFolder

""
"Creating 7z file $DestinationFile"
""
7z a $DestinationFile $SourceFolder