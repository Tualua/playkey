$ToolsDrive = Get-Volume -FileSystemLabel Tools
$ToolsLetter = $ToolsDrive.DriveLetter
$MinerPath = $ToolsLetter + ":\gminer\"
Copy-Item $MinerPath -Destination 'C:\Temp\gminer\' -Recurse
