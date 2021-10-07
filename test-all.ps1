Function Invoke-Tests {
    $version = $args[0]
    $venvName = "." + $version + ".venv"
    Write-Host "*** Testing with Python "$version" ***" -ForegroundColor yellow
    & "$venvName\Scripts\python.exe" .\test_examples.py
}

Invoke-Tests 3.6
Invoke-Tests 3.7
Invoke-Tests 3.8
Invoke-Tests 3.9
Invoke-Tests "3.10"
