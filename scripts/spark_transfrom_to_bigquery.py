import pyspark

from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

from pyspark.sql import types
import pyspark.sql.functions as F

from dotenv import load_dotenv
load_dotenv()

SPARK_GCS_JAR = '/workspaces/linkedin_job_analysis/airflow/gcs-connector-hadoop3-latest.jar'
SPARK_BQ_JAR = '/workspaces/linkedin_job_analysis/airflow/spark-3.5-bigquery-0.37.0.jar'

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", f'{SPARK_GCS_JAR}, {SPARK_BQ_JAR}') \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "/workspaces/linkedin_job_analysis/terraform/creds.json") \
    .set('temporaryGcsBucket', 'linkedin_job_bucket') \
    .set("viewsEnabled","true") \
    .set("materializationDataset","linkedin_job_bq")


sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", "/workspaces/linkedin_job_analysis/terraform/creds.json")
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

skills_df = spark.read.parquet('gs://linkedin_job_bucket/linkedin_dataset/job_skills.parquet')
skills_df = skills_df.withColumnRenamed("job_link","job_link_doubled")

job_posting_df = spark.read \
    .parquet('/workspaces/linkedin_job_analysis/airflow/linkedin_job_postings.parquet', header=True)

linkedin_jobs_df = job_posting_df.join(skills_df, job_posting_df.job_link == skills_df.job_link_doubled, "inner")
linkedin_jobs_df = linkedin_jobs_df.drop(linkedin_jobs_df.job_link_doubled, linkedin_jobs_df.got_ner, linkedin_jobs_df.is_being_worked)
linkedin_jobs_df = linkedin_jobs_df.dropna()

most_popular_jobs = linkedin_jobs_df.groupBy("job_title").count() \
    .orderBy(F.col("count").desc()).limit(15)

top_companies = linkedin_jobs_df.groupBy("company").count() \
    .orderBy(F.col("count").desc()).limit(15)
    
most_popular_locations_us = linkedin_jobs_df.filter(linkedin_jobs_df.search_country.contains('United States')) \
    .groupBy("job_location").count().orderBy(F.col("count").desc()).limit(30)

job_type = linkedin_jobs_df.groupBy("job_type").count() \
    .orderBy(F.col("count").desc()).limit(3)

table_list = [most_popular_jobs, top_companies, most_popular_locations_us, job_type]
table_names = ['most_popular_jobs', 'top_companies', 'most_popular_locations_us', 'job_type']

for el in range(len(table_list)):
    table_list[el].write.format('bigquery') \
        .option('table', f"linkedin_job_bq.{table_names[el]}") \
        .option("parentProject", "linkedin-jobs-418420") \
        .mode('append') \
        .save()