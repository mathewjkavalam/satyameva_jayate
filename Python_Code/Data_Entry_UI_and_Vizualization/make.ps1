param (
    [string]$target  # The target command (e.g., install, run)
)

$makefile = "Makefile"
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Check if the Makefile exists
if (-Not (Test-Path $makefile)) {
    Write-Host "Error: Makefile not found in the current directory."
    exit 1
}

# Read the Makefile content
$lines = Get-Content $makefile
$commands = @{}
$currentTarget = $null

# Parse the Makefile
foreach ($line in $lines) {
    if ($line -match "^(\w+):$") {
        $currentTarget = $matches[1]
        $commands[$currentTarget] = @()
    }
    elseif ($currentTarget -and $line -match "^\s+(.+)$") {
        $commands[$currentTarget] += $matches[1]
    }
}

# Execute the command if it exists
if ($commands.ContainsKey($target)) {
    foreach ($cmd in $commands[$target]) {
        try {
            Write-Host "Executing: $cmd"
            Invoke-Expression $cmd  # Run the command
        }
        catch {
            "An error occurred that could not be resolved."
        }
        finally{
            # move on...
        }
   }
} else {
    Write-Host "Error: Target '$target' not found in Makefile."
    exit 1
}
