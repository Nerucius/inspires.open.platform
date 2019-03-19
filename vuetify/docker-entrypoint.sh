#!/bin/sh

echo "Cleaning old files, skipping static/"
find . -maxdepth 1 | grep -v "^.$" | grep -v "static" | xargs rm -r

echo "Begin Vue Build"
npm run build:docker