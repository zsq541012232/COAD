# The dataset and code implementation of COAD

## Congratulations! We have published our research paper on the conference of APSEC2023!

Here is the link: https://conf.researchr.org/details/apsec-2023/apsec-2023-technical-track/39/Effective-Anomaly-Detection-for-Microservice-Systems-with-Real-Time-Feature-Selection

## The [data](https://github.com/zsq541012232/COAD/tree/main/data) folder

The folder [data](https://github.com/zsq541012232/COAD/tree/main/data) contains the dataset produced by a real deployed microservice system [hipstershop](https://github.com/abruneau/hipstershop).

There are three testbeds' data: dataset1, dataset2, dataset3.

Each testbeds' data contains days of multivariate time series. (For example: instance1 is a day's data).

Each day's data folder contains three files: ground_truth.csv, test_df.csv, and train_df.csv.

Ground_truth.csv contains the true faults happening time; Train_df.csv contains the normal state data for training anomaly detection models; Test_df.csv contains the data for anomaly detection (i.e., it contains the injected true faults as the same as the true faults in the Ground_truth.csv).


## The [functions](https://github.com/zsq541012232/COAD/tree/main/functions) folder

The main realization of COAD is in the folder [detection](https://github.com/zsq541012232/COAD/tree/main/functions/detection); the helper functions are in the folder [utils](https://github.com/zsq541012232/COAD/tree/main/functions/utils).


## The [result](https://github.com/zsq541012232/COAD/tree/main/result) and [result_all](https://github.com/zsq541012232/COAD/tree/main/result_all) folders

The [result](https://github.com/zsq541012232/COAD/tree/main/result) folder is the path of the output of the anomaly detection; the [result_all](https://github.com/zsq541012232/COAD/tree/main/result_all) folder is the history result repository, because we ran the experiment serveral times, and the history results are moved from the folder [result](https://github.com/zsq541012232/COAD/tree/main/result) to [result_all](https://github.com/zsq541012232/COAD/tree/main/result_all).


## The [script](https://github.com/zsq541012232/COAD/tree/main/script) folder

This folder is as important as the folder 'functions', becasue it contains the entrance of COAD's experiment. 

The folder [analyze](https://github.com/zsq541012232/COAD/tree/main/script/analyze) provide the script for analyzing the anomaly detection results (For example, output the M-value or R-value of a result).

The folder [derection](https://github.com/zsq541012232/COAD/tree/main/script/detection) provide the script for executing the anomaly detection for a day's data: you can choose to use COAD or the original anomaly detection algorithm; you can decide which testbed or which day to detect anomalies; you can choose the anomaly detection algorithm and the metaheuristic algorithm.

The folder [plan](https://github.com/zsq541012232/COAD/tree/main/script/plans) records the experiment's plan.
