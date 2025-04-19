param (
    [string]$JsonReportPath,
    [double]$CoverageThreshold
)

try {
    $jsonContent = Get-Content $JsonReportPath -Raw | ConvertFrom-Json
} catch {
    Write-Error "Failed to read or parse JSON report: $_"
    exit 1
}

$coverageBelowThreshold = $false

$nonExperimentalAssemblies = [System.Collections.Generic.HashSet[string]]::new()

$assembliesCollection = @(
    'Microsoft.SemanticKernel.Abstractions'
    'Microsoft.SemanticKernel.Core'
    'Microsoft.SemanticKernel.PromptTemplates.Handlebars'
    'Microsoft.SemanticKernel.Connectors.OpenAI'
    'Microsoft.SemanticKernel.Connectors.AzureOpenAI'
    'Microsoft.SemanticKernel.Yaml'
    'Microsoft.SemanticKernel.Agents.Abstractions'
    'Microsoft.SemanticKernel.Agents.Core'
    'Microsoft.SemanticKernel.Agents.OpenAI'
)

foreach ($assembly in $assembliesCollection) {
    $nonExperimentalAssemblies.Add($assembly)
}

function Get-FormattedValue {
    param (
        [float]$Coverage,
        [bool]$UseIcon = $false
    )
    try {
        $formattedNumber = "{0:N1}" -f $Coverage
        $icon = if (-not $UseIcon) { "" } elseif ($Coverage -ge $CoverageThreshold) { '✅' } else { '❌' }
        return "$formattedNumber% $icon"
    } catch {
        Write-Error "Failed to format coverage value: $_"
        return "N/A"
    }
}

try {
    $lineCoverage = $jsonContent.summary.linecoverage
    $branchCoverage = $jsonContent.summary.branchcoverage
} catch {
    Write-Error "Failed to extract coverage summary: $_"
    exit 1
}

$totalTableData = [PSCustomObject]@{
    'Metric'          = 'Total Coverage'
    'Line Coverage'   = Get-FormattedValue -Coverage $lineCoverage
    'Branch Coverage' = Get-FormattedValue -Coverage $branchCoverage
}

$totalTableData | Format-Table -AutoSize

$assemblyTableData = @()

foreach ($assembly in $jsonContent.coverage.assemblies) {
    try {
        $assemblyName = $assembly.name
        $assemblyLineCoverage = $assembly.coverage
        $assemblyBranchCoverage = $assembly.branchcoverage

        $isNonExperimentalAssembly = $nonExperimentalAssemblies -contains $assemblyName

        if ($isNonExperimentalAssembly -and ($assemblyLineCoverage -lt $CoverageThreshold -or $assemblyBranchCoverage -lt $CoverageThreshold)) {
            $coverageBelowThreshold = $true
        }

        $assemblyTableData += [PSCustomObject]@{
            'Assembly Name' = $assemblyName
            'Line'          = Get-FormattedValue -Coverage $assemblyLineCoverage -UseIcon $isNonExperimentalAssembly
            'Branch'        = Get-FormattedValue -Coverage $assemblyBranchCoverage -UseIcon $isNonExperimentalAssembly
        }
    } catch {
        Write-Error "Failed to process assembly $assemblyName: $_"
    }
}

$sortedTable = $assemblyTableData | Sort-Object {
    $nonExperimentalAssemblies -contains $_.'Assembly Name'
} -Descending

$sortedTable | Format-Table -AutoSize

if ($coverageBelowThreshold) {
    Write-Host "Code coverage is lower than defined threshold: $CoverageThreshold. Stopping the task."
    exit 1
}

# Fix Errors
try {
    & "./fix-errors.sh"
} catch {
    Write-Error "Failed to run fix-errors.sh: $_"
    exit 1
}
