function Show-Tree {
    param(
        [string]$Path = ".",
        [string[]]$Exclude = @(".git", ".venv", ".vs", "node_modules", "__pycache__",".pytest_cache")
    )

    function Write-Tree {
        param(
            [string]$CurrentPath,
            [string]$Prefix = ""
        )

        $items = Get-ChildItem -LiteralPath $CurrentPath |
            Where-Object { $_.Name -notin $Exclude } |
            Sort-Object @{Expression = { -not $_.PSIsContainer }}, Name

        for ($i = 0; $i -lt $items.Count; $i++) {
            $item = $items[$i]
            $last = ($i -eq $items.Count - 1)

            $branch = if ($last) { "└── " } else { "├── " }
            Write-Host "$Prefix$branch$($item.Name)"

            if ($item.PSIsContainer) {
                $nextPrefix = if ($last) { "$Prefix    " } else { "$Prefix│   " }
                Write-Tree -CurrentPath $item.FullName -Prefix $nextPrefix
            }
        }
    }

    $resolved = Resolve-Path $Path
    Write-Host (Split-Path $resolved -Leaf)
    Write-Tree -CurrentPath $resolved
}

if ($MyInvocation.InvocationName -ne '.') {
    Show-Tree
}