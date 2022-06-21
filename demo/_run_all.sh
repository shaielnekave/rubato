# Use ctrl+z to stop the script. ctrl+c won't work.
# Run it from the demo folder with: ./_run_all.sh
# Does not work if you run it from outside the demo folder.

files=`ls ./*.py`


for file in $files
do
    echo "Running $file"
    if command -v python &> /dev/null
    then
        timeout --preserve-status 5s python $file
    else
        timeout --preserve-status 5s python3 $file
    fi

    retVal=$?
    if [ "$retVal" != "143"  ] && [ "$retVal" != "124" ] && [ "$retVal" != "0" ]
    then
        exit 1
    fi
done
