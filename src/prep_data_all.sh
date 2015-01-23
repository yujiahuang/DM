# sh prep_data.sh (1)dataset (2)year_as_test
date

python split_data.py $1 $2
cp ./data/past_data ./data/sample_data
python gen_feature.py ./data/past_data ./data/ans_data ./data/sample_data 1
# gen test data

# rm [_temp_blah data]
date