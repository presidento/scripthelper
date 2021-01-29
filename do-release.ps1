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

Write-Step "Bootstrap Python environments and activate one"
.\bootstrap.ps1
Invoke-Command { .\test-all.ps1 }

Write-Step "Install build dependencies and build the release"
Invoke-Command { python -m pip install --upgrade setuptools wheel pip twine }
Invoke-Command { python setup.py sdist bdist_wheel }

Write-Step "Upload release to pypi"
Invoke-Command { python -m twine upload dist/* }
