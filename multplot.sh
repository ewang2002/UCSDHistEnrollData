# Check if the help argument is provied
if [ "$1" = "-h" ] || [ "$1" = "--help" ]
then
    echo "Usage: multplot.sh [OPTION]..."
    echo "Cleans & plots enrollment datasets. By default, this cleans and plots the datasets."
    echo "  -h, --help      display this help and exit"
    echo "    --noplot      do not plot the datasets"
    echo "     --nocat      do not clean the datasets"
    exit 0
fi

categorize=1
plot=1

# Check if any of the arguments is "noplot" or "nocat"
for arg in $@
do
    if [ $arg = "--noplot" ]
    then
        plot=0
    fi
    if [ $arg = "--nocat" ]
    then
        categorize=0
    fi
done

# Define an array containing S122, S222, FA22, S122D
terms=("FA22" "S122" "S222" "S122D")

# Loop through each term
for term in ${terms[@]}; do
    echo "================== Processing $term. =================="
    # Check if we should categorize
    if [ $categorize -eq 1 ]
    then
        echo -e "\tCleaning raw CSVs."
        python clean_raw_csvs.py $term
        echo -e "\tCategorizing enroll data."
        python enroll_data_cleaner.py $term
    fi

    # Check if we should plot
    if [ $plot -eq 1 ]
    then
        echo -e "\tPlotting overall data."
        python plot.py $term o
        echo -e "\tPlotting section data."
        python plot.py $term s
    fi
done
