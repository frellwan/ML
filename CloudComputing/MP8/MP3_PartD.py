from pyspark import SparkContext, SQLContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType

sc = SparkContext()
sqlContext = SQLContext(sc)

####
# 1. Setup (10 points): Download the gbook file and write a function to load it in an RDD & DataFrame
####

# RDD API
# Columns:
# 0: place (string), 1: count1 (int), 2: count2 (int), 3: count3 (int)


# Spark SQL - DataFrame API


mp8schema = StructType([
    StructField("word",  StringType(), True),
    StructField("count1", IntegerType(), True),
    StructField("count2", IntegerType(), True),
    StructField("count3", IntegerType(), True)
    ])


df = sqlContext.read.format("csv").option("delimiter", "\t") \
        .schema(mp8schema) \
        .load(r"gbooks")

df.createOrReplaceTempView("df")
sqlContext.sql("SELECT word, count(1) FROM df GROUP BY word ORDER BY count(1) DESC").show(n=3)





