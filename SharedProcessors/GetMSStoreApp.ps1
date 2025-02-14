# Download App with dependencies from MS store to install offline. 
# PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%cd%\GetMSStoreApp.ps1'"

param(
    [Parameter(mandatory=$true)][string]$app_url,
    [Parameter(mandatory=$true)][string]$dl_dir,
    [Parameter(mandatory=$false)][string]$prop_file
);

#Create a version string without delimiters
#https://serverfault.com/questions/1018220/how-do-i-install-an-app-from-windows-store-using-powershell

#Usage:
# Download-AppxPackage "https://apps.microsoft.com/detail/9NKSQGP7F2NH" "$ENV:USERPROFILE\Desktop"
# download WhatsApp  

# Speedup Download with Invoke-WebRequest
#$ProgressPreference = 'SilentlyContinue'

<# function Download-AppxPackage {
[CmdletBinding()]
param (
  [string]$Uri,
  [string]$Path = "."
) #>
  
#$Uri = "https://apps.microsoft.com/detail/9NKSQGP7F2NH"
  process {
    #$Path = (Resolve-Path $Path).Path
	$Path = (Resolve-Path $dl_dir).Path
    #Get Urls to download
    $WebResponse = Invoke-WebRequest -UseBasicParsing -Method 'POST' -Uri 'https://store.rg-adguard.net/api/GetFiles' -Body "type=url&url=$app_url&ring=Retail" -ContentType 'application/x-www-form-urlencoded'
    $LinksMatch = $WebResponse.Links | where {$_ -like '*.appx*' -or $_ -like '*.appxbundle*' -or $_ -like '*.msix*' -or $_ -like '*.msixbundle*'} | where {$_ -like '*_neutral_*' -or $_ -like "*_"+$env:PROCESSOR_ARCHITECTURE.Replace("AMD","X").Replace("IA","X")+"_*"} | Select-String -Pattern '(?<=a href=").+(?=" r)'
    $DownloadLinks = $LinksMatch.matches.value 

    function Resolve-NameConflict{
    #Accepts Path to a FILE and changes it so there are no name conflicts
    param(
    [string]$Path
    )
        $newPath = $Path
        if(Test-Path $Path){
            $i = 0;
            $item = (Get-Item $Path)
            while(Test-Path $newPath){
                $i += 1;
                $newPath = Join-Path $item.DirectoryName ($item.BaseName+"($i)"+$item.Extension)
            }
        }
        return $newPath
    }
	#Initialize $FileList
	$FileList = ""
	# Speedup Download with Invoke-WebRequest
	$ProgressPreference = 'SilentlyContinue'
    #Download Urls
    foreach($url in $DownloadLinks){
		echo $url
        $FileRequest = Invoke-WebRequest -Uri $url -UseBasicParsing #-Method Head
        $FileName = ($FileRequest.Headers["Content-Disposition"] | Select-String -Pattern  '(?<=filename=).+').matches.value
        $FilePath = Join-Path $Path $FileName; $FilePath = Resolve-NameConflict($FilePath)
        [System.IO.File]::WriteAllBytes($FilePath, $FileRequest.content)
		$FileList = $FileList + $FileName + "|" 
        echo $FilePath
    }
	#return $FileList $url
	return (-join($FileList, $url))
  }

