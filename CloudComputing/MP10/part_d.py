from pyspark.ml.classification import RandomForestClassifier
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.linalg import Vectors

sc = SparkContext()
sqlContext = SQLContext(sc)


def predict(df_train, df_test):
    # TODO: Train random forest classifier

    # Hint: Column names in the given dataframes need to match the column names
    # expected by the random forest classifier `train` and `transform` functions.
    # Or you can alternatively specify which columns the `train` and `transform`
    # functions should use

    # Result: Result should be a list with the trained model's predictions
    # for all the test data points
    rf = RandomForestClassifier(featuresCol = 'features', labelCol = 'label',
                                numTrees = 25, maxDepth = 15, seed = 420)
    model = rf.fit(df_train)
    prediction = model.transform(df_test).select('prediction')
    predList =[int(row.prediction) for row in predictions.collect()]
    return predList


def main():
    raw_training_data = sc.textFile("dataset/training.data")

    # TODO: Convert text file into an RDD which can be converted to a DataFrame
    # Hint: For types and format look at what the format required by the
    # `train` method for the random forest classifier
    # Hint 2: Look at the imports above
    def rddTrain(line):
        line = line.split(',')
        label = float(line[-1])
        features = Vectors.dense(line[:-1])
        return (label, features)

    rdd_train = raw_training_data.map(lambda line: rddTrain(line))

    # TODO: Create dataframe from the RDD
    df_train = rdd_train.toDF(["label", "features"])

    raw_test_data = sc.textFile("dataset/test-features.data")

    def rddTest(line):
        line = line.split(',')
        features = Vectors.dense(line[:])
        return (features,)
    # TODO: Convert text file lines into an RDD we can use later
    rdd_test = raw_test_data.map(lambda line: rddTest(line))

    # TODO:Create dataframe from RDD
    df_test = rdd_test.toDF(['features'])

    predictions = predict(df_train, df_test)

    # You can take a look at dataset/test-labels.data to see if your
    # predictions were right
    for pred in predictions:
        print(int(pred))


if __name__ == "__main__":
    main()