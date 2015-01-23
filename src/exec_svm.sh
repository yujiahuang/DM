lib/libsvm/tools/subset.py -s 0 data/feature_data 1600 data/train_data data/test_data
lib/libsvm/svm-train -s 2 -g 0.8 -n 0.066 data/train_data
# lib/libsvm/svm-train -s 2 -g 0.0001 -n 0.5 data/train_data
# lib/libsvm/svm-train -s 0 -c 100000 data/train_data
lib/libsvm/svm-predict data/test_data train_data.model predict_output
