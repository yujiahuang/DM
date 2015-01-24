lib/libsvm/tools/subset.py -s 0 data/feature_data $1 data/train_data data/test_data

python gen_half_data.py data/train_data data/train_data_half
python gen_half_data.py data/test_data data/test_data_half

lib/libsvm/svm-scale -u 10 -l -10 data/train_data_half > data/train_data_half_scale
lib/libsvm/svm-scale -u 10 -l -10 data/test_data_half > data/test_data_half_scale

# lib/libsvm/svm-train -s 2 -g 0.8 -n 0.066 data/train_data
# lib/libsvm/svm-train -s 2 -g 0.0001 -n 0.5 data/train_data
# lib/libsvm/svm-train -s 0 -c 100000 data/train_data
lib/libsvm/svm-train -g 3.0517578125e-05 -c 128 data/train_data_half_scale
lib/libsvm/svm-predict data/test_data_half_scale train_data_half_scale.model predict_output
