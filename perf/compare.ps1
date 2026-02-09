param($base,$current,$threshold)

$old = (Get-Content $base | Measure-Object).Count
$new = (Get-Content $current | Measure-Object).Count

$diff = (($new - $old) / $old) * 100

if ($diff -gt $threshold) {
    Write-Error "Performance degraded by $diff%"
    exit 1
}