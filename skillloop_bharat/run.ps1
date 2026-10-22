Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting SkillLoop Bharat Prototype" -ForegroundColor Yellow
Write-Host "  Learn from Real Problems. Build Real Skills." -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
& "$env:USERPROFILE\.local\bin\uv.exe" run --with flask python app.py
