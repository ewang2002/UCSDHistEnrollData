$terms = @("FA22", "S122", "S222")

Write-Output "`tCloning..."
git clone https://github.com/ewang2002/UCSDHistEnrollData
Set-Location UCSDHistEnrollData

foreach ($term in $terms) {
    Write-Output "================== Processing $term. =================="
    Write-Output "`tCleaning raw CSVs."
    python clean_raw_csvs.py $term

    Write-Output "`tCategorizing enroll data."
    python enroll_data_cleaner.py $term

    Write-Output "`tPlotting overall data."
    python plot.py $term o
    Write-Output "`tPlotting section data."
    python plot.py $term s
}

# commit
Write-Output "`tCommitting changes."
git add .
git commit -m (Get-Date -UFormat "%B %d, %Y - update (plot, automated)")
git push