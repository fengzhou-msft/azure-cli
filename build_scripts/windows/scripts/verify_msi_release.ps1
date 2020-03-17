Function Get-RedirectedUrl {
    Param (
        [Parameter(Mandatory=$true)]
        [String]$url
    )
    $request = [System.Net.WebRequest]::Create($url)
    $request.AllowAutoRedirect=$true
    try{
        $response=$request.GetResponse()
        $response.ResponseUri.AbsoluteUri
        $response.Close()
    }
    catch{
    "ERROR: $_"
    }
}

$FileName = [System.IO.Path]::GetFileName((Get-RedirectedUrl "https://aka.ms/installazurecliwindows"))

$ActualVersion = $FileName -replace '\D+([\d.]+\d+)\D+','$1'
echo "actual version:${ActualVersion}"
echo "expected version:${Env:CLI_VERSION}"

if ($ActualVersion -ne $Env:CLI_VERSION) {
    echo "The download link has not been updated to the latest version!"
    exit 1
} else {
    echo "The download link is update to date."
}

Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi

$asig = Get-AuthenticodeSignature .\AzureCLI.msi
$subject= $asig.SignerCertificate.Subject
if ($subject -ne "CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US") {
    echo "The package is not properly signed."
    exit 1
} else {
    echo "The package is signed by Microsoft Corporation."
}