Function Write-Step {
    Write-Host -NoNewline  "*** " $args[0] " *** (Press ENTER)" -ForegroundColor yellow
    Read-Host
}
$ErrorActionPreference = "Stop"
function Invoke-Command {
    param ([scriptblock]$ScriptBlock)
    Write-Host "Run " $ScriptBlock -ForegroundColor green
    & @ScriptBlock
    if ($lastexitcode -ne 0) {
        Write-Host "ERROR happened, exiting..."
        exit $lastexitcode
    }
}

Write-Step "Delete build folders"
Remove-Item -Recurse -Force -ErrorAction Ignore build
Remove-Item -Recurse -Force -ErrorAction Ignore dist

Write-Step "Activate Python environment"
.venv\Scripts\activate.ps1

Write-Step "Install dependencies, the script itself and run tests"
Invoke-Command { python -m pip install --upgrade setuptools wheel pip twine }
Invoke-Command { python -m pip install --upgrade . }
Invoke-Command { python test_examples.py }

Write-Step "Build the release"
Invoke-Command { python setup.py sdist bdist_wheel }

Write-Step "Uploading release to pypi"
Invoke-Command { python -m twine upload dist/* }
