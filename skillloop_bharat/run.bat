@echo off
echo ========================================================
echo   Starting SkillLoop Bharat Prototype
echo   Learn from Real Problems. Build Real Skills.
echo ========================================================
echo.
"%USERPROFILE%\.local\bin\uv.exe" run --with flask python app.py
pause
