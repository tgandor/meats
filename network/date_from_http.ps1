
# you may be looking for this:
# Set-ExecutionPolicy RemoteSigned

# or maybe this:
# PowerShell.exe -ExecutionPolicy Bypass -File .\date_from_http.ps1
# PowerShell.exe -ExecutionPolicy Unrestricted -File .\date_from_http.ps1
# type date_from_http.ps1 | PowerShell.exe -noprofile -

# or paste this:
# set-date -date (wget google.com).Headers['Date']

# Do You Trust this Computer?
$response = wget google.com

$date = $response.Headers['Date']
echo Changing date to $date
set-date -date $date
