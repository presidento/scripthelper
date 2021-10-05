Function Initialize-Python {
    $version = $args[0]
    $venvName = "." + $version + ".venv"
    Write-Host "*** Setting up Python "$version" environment ***" -ForegroundColor yellow
    If (-not (Test-Path $venvName)) { py -$version -m venv $venvName }
    & "$venvName\Scripts\python.exe" -m pip install pip --quiet --upgrade
    & "$venvName\Scripts\python.exe" -m pip install . --upgrade
}

Initialize-Python 3.7
Initialize-Python 3.8
Initialize-Python 3.9
Initialize-Python "3.10"

.\.3.7.venv\Scripts\activate.ps1
