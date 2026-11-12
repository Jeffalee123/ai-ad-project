param(
    [Parameter(Mandatory=$true)] [string]$Username,
    [Parameter(Mandatory=$true)] [string]$FirstName,
    [Parameter(Mandatory=$true)] [string]$LastName,
    [Parameter(Mandatory=$true)] [string]$Department,
    [Parameter(Mandatory=$true)] [string]$Password,
    [switch]$DryRun
)

if ($DryRun) {
    Write-Host "[DRY-RUN] Would create AD User: $FirstName $LastName ($Username) | Dept: $Department"
    exit 0
}

$SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force

New-ADUser -Name "$FirstName $LastName" `
           -SamAccountName $Username `
           -UserPrincipalName "$Username@yourdomain.local" `
           -GivenName $FirstName `
           -Surname $LastName `
           -Department $Department `
           -AccountPassword $SecurePassword `
           -Enabled $true `
           -PasswordNeverExpires $false `
           -ChangePasswordAtLogon $true

Add-ADGroupMember -Identity $Department -Members $Username
Write-Host "Successfully provisioned user $Username and added to group $Department."
