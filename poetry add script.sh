Get-Content requirements.txt |
  Where-Object { $_ -and ($_ -notmatch '^\s*#') } |
  ForEach-Object { poetry add $_ }