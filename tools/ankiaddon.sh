# This Code was originally commited to https://github.com/ThoreBor/Anki_Leaderboard by https://github.com/zjosua
#!/bin/bash

set -e

target="build/WordFinder.ankiaddon"

if [ ! -e "manifest.json" ]
then
    echo "manifest.json is missing."
    echo "Make sure you are running this script from the project root."
    exit
fi

if [ -e $target ]
then
    rm -rf $target
fi

mkdir -p build

echo "Building ankiaddon file..."

zip $target *.py forms/*.py *.json README.md LICENSE

echo "Saved package at $target"
