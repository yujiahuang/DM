# sh prep_data.sh (1)dataset (2)year_as_test (3)num (4)[-s]

python trans_data.py $1 $2
python lib/libsvm/tools/subset.py -s ${4:-0} ./data/_temp_past_data ${3} > ./data/_temp_sample_data
python clean_data.py ./data/_temp_sample_data ./data/sample_data
python gen_feature.py ./data/past_data ./data/ans_data ./data/sample_data ./data/feature_data
# gen test data

# rm [_temp_blah data]