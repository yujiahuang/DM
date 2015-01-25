# sh exec_svm.sh (1)number to train

lib/libsvm/tools/subset.py ./data/feature_data_scale_past_half $1 ./data/feature_data_scale_past_half_train ./data/feature_data_scale_past_half_test

# lib/libsvm/svm-train -s 2 -g 0.8 -n 0.066 data/train_data
# lib/libsvm/svm-train -s 2 -g 0.0001 -n 0.5 data/train_data
# lib/libsvm/svm-train -s 0 -c 100000 data/train_data
lib/libsvm/svm-train -g 0.0001220703125 -c 2048.0 ./data/feature_data_scale_past_half_train
lib/libsvm/svm-predict data/feature_data_scale_past_half_test feature_data_scale_past_half_train.model predict_output
