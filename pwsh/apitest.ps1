echo "----------------------------- SEKCJE -----------------------------"
invoke-webrequest -Uri "127.0.0.1:8000/api/section" -Method Get | ConvertFrom-Json

echo "----------------------------- POSTY -----------------------------"
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/post" -Method Get |
ConvertFrom-Json |
Format-Table -AutoSize

echo "----------------------------- KOMENTARZE -----------------------------"
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/reply" -Method Get | ConvertFrom-Json | Format-Table -AutoSize
