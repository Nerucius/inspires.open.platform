#!/bin/sh

# echo "Cleaning old files, skipping static/"
# find ./dist/ -maxdepth 1 | grep -v "^./dist/$" | grep -v "static" | xargs rm -r

echo "Begin Vue Build"
# npm update caniuse-lite browserslist
npm run build:docker
