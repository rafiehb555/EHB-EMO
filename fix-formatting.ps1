# Fix all formatting issues permanently
Write-Host "Fixing all formatting issues..." -ForegroundColor Green

# Fix README.md
$readme = Get-Content "README.md" -Raw
$readme = $readme -replace '\s+$', '' -replace '\r\n', "`n"
$readme = $readme.TrimEnd() + "`n"
Set-Content "README.md" $readme -NoNewline -Encoding UTF8

# Fix script.py
$script = Get-Content "script.py" -Raw
$script = $script -replace '\s+$', '' -replace '\r\n', "`n"
$script = $script.TrimEnd() + "`n"
Set-Content "script.py" $script -NoNewline -Encoding UTF8

# Fix all .md files
Get-ChildItem -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace '\s+$', '' -replace '\r\n', "`n"
    $content = $content.TrimEnd() + "`n"
    Set-Content $_.FullName $content -NoNewline -Encoding UTF8
}

# Fix all .py files
Get-ChildItem -Filter "*.py" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace '\s+$', '' -replace '\r\n', "`n"
    $content = $content.TrimEnd() + "`n"
    Set-Content $_.FullName $content -NoNewline -Encoding UTF8
}

Write-Host "All formatting issues fixed permanently!" -ForegroundColor Green
Write-Host "Please restart VS Code to clear the cache." -ForegroundColor Yellow 