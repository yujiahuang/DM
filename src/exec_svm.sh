lib/libsvm/tools/subset.py -s 0 data/feature_data 1600 data/train_data data/test_data
lib/libsvm/svm-train -s 2 -g 0.4 -n 0.1 data/train_data
lib/libsvm/svm-predict data/test_data train_data.model predict_output
