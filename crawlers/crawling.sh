#!/bin/bash

# Path to the nested folder
nested_folder="src"
data_folder="../data"

# Move to the nested folder
cd "$nested_folder" || exit

# Execute command in the nested folder
scrapy crawl lawnet_crawler -o "$data_folder/lawnet_datasets.json"
scrapy crawl thuvienphapluat_crawler -o "$data_folder/thuvienphapluat_datasets.json"
scrapy crawl  hieuluat_crawler -o "$data_folder/hieuluat_datasets.json"

# output: crawlers/data total 1437 sample
