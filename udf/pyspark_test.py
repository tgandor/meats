#!/usr/bin/env python

# Import required libraries
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder.getOrCreate()

# Create SparkContext
sc = spark.sparkContext

# Create a sample DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35), ("Dave", 40)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Filter rows based on a condition
filtered_df = df.filter(df.Age > 30)

# Display the filtered DataFrame
filtered_df.show()
