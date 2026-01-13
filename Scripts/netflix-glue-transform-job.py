import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_date, split, trim


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)


df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3://netflix-data-001/processed/netflix_titles.csv")

# Transformations
df_clean = (
    df
    .withColumn("date_added", to_date(col("date_added"), "MMMM d, yyyy"))
    .withColumn("country", trim(col("country")))
    .withColumn("listed_in", split(col("listed_in"), ","))
    .dropDuplicates(["show_id"])
)

# Write Parquet to curated layer
df_clean.write \
    .mode("overwrite") \
    .parquet("s3://netflix-data-001/curated/netflix_titles/")

job.commit()
