# Check if any arguments were passed in
if [ $# -eq 0 ]; then
    echo "Usage: run.sh <term>"
    exit 1
fi

# Run both scripts
python clean_raw_csvs.py $1
python enroll_data_cleaner.py $1

exit 0