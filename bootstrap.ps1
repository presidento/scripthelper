Function Initialize-Python {
    $version = $args[0]
    $venvName = "." + $version + ".venv"
    Write-Host "*** Setting up Python "$version" environment ***" -ForegroundColor yellow
    If (-not (Test-Path $venvName)) { py -$version -m venv $venvName }
    & "$venvName\Scripts\python.exe" -m pip install pip wheel --quiet --upgrade
    & "$venvName\Scripts\python.exe" -m pip install . --upgrade --use-feature=in-tree-build
}

Initialize-Python 3.6
Initialize-Python 3.7
Initialize-Python 3.8
Initialize-Python 3.9
Initialize-Python "3.10"

.\.3.7.venv\Scripts\activate.ps1
