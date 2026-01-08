# Prompt for author details
$authorName  = Read-Host "Enter AUTHOR NAME"
$authorEmail = Read-Host "Enter AUTHOR EMAIL"

# Prompt for backdated commit time
$customDate = Read-Host "Enter AUTHOR DATE (e.g. 2025-01-07T11:11:00 or '2 weeks ago')"

# Prompt for commit message
$commitMessage = Read-Host "Enter commit message"

Write-Host ""
Write-Host "⚠️  Creating backdated commit as:" -ForegroundColor Yellow
Write-Host "   Name : $authorName"
Write-Host "   Email: $authorEmail"
Write-Host "   Date : $customDate"
Write-Host ""

# Set environment variables for this commit
$env:GIT_AUTHOR_NAME     = $authorName
$env:GIT_AUTHOR_EMAIL    = $authorEmail
$env:GIT_AUTHOR_DATE     = $customDate
$env:GIT_COMMITTER_DATE  = $customDate

# Run the git commit
git commit -m "$commitMessage"

# Clean up so Git doesn’t keep lying later
Remove-Item env:GIT_AUTHOR_NAME
Remove-Item env:GIT_AUTHOR_EMAIL

Write-Host ""
Write-Host "✅ Commit complete. Timeline successfully fucked with." -ForegroundColor Green
