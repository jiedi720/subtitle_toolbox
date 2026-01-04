cd "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SubtitleToolbox"

# Set username for current project
git config user.name "jiedi720"

# (Optional) Set global username
git config --global user.name "jiedi720"

# Set UTF8 encoding for display
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "--- Preparing to upload SubtitleToolbox v3.0 ---" -ForegroundColor Cyan

# Add changes
git add .

# Get user input
$msg = Read-Host "Enter update message (press Enter for default 'Daily update')"
if ($msg -eq "") { $msg = "Daily update" }

# Commit
git commit -m $msg

# Push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Update successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Update failed, please check network." -ForegroundColor Red
}

pause