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

df2 = df.select("word", "count1").distinct().limit(1000)
df2.createOrReplaceTempView('gbooks2')

print(sqlContext.sql("SELECT a.count1, b.count1 FROM gbooks2 AS a, gbooks2 AS b WHERE a.count1 = b.count1").count())



