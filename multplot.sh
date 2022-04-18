# Define an array containing S122, S222, S322, and SP22D
terms=("S122" "S222" "SP22D")

# Loop through each term
for term in ${terms[@]}; do
    echo "================== Processing $term. =================="
    echo -e "\tCleaning raw CSVs."
    python clean_raw_csvs.py $term
    echo -e "\tCategorizing enroll data."
    python enroll_data_cleaner.py $term
    echo -e "\tPlotting overall data."
    python plot.py $term o
    echo -e "\tPlotting section data."
    python plot.py $term s
done