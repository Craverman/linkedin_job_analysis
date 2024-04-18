# Linkedin Job Analysis
![image](https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/LinkedIn_Logo.svg/1280px-LinkedIn_Logo.svg.png)
### _“Catch a man a fish, and you can sell it to him. Teach a man to fish, and you ruin a wonderful business opportunity.”_

The dynamic nature of the job market in the United States poses significant challenges for job seekers, employers, educators, and trainers. The lack of real-time insights into the skills required for jobs, top companies in the market, popular job roles, and hiring locations can hinder individuals and organizations in making informed decisions regarding recruitment, talent development, and career planning.

In light of this, the research aims to analyze the LinkedIn job dataset from January 1, 2024, to March 31, 2024, in the United States to identify and understand the trends shaping the job market during this period. By examining the skills required for jobs, top companies posting job listings, most popular job roles, and hiring locations, the research seeks to provide actionable insights that can empower stakeholders to optimize their recruitment strategies, skill development initiatives, and career planning efforts.

## Technologies
- Cloud - [**Google Cloud Platform**](https://cloud.google.com)
- Infrastructure as Code software (IaC) - [**Terraform**](https://www.terraform.io)
-  Containerization - [**Docker**](https://www.docker.com), [**Docker Compose**](https://docs.docker.com/compose/)
- Workflow Orchestration - [**Airflow**](https://airflow.apache.org)
- Batch processing - [**Apache Spark**](https://spark.apache.org/docs/latest/api/python/)
- Data Lake - [**Google Cloud Storage**](https://cloud.google.com/storage)
- Data Warehouse - [**BigQuery**](https://cloud.google.com/bigquery)
- Data Visualization - [**Looker Studio (Google Data Studio)**](https://lookerstudio.google.com/overview?)

## Data Pipeline 
[**Linkedin jobs and skill 2024 dataset**](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024) -> format to .parquet -> to GCS -> transform data with pyspark -> to BigQuery -> to LookerStudio

![image](https://i.ibb.co/ZJZfw7h/drawio.png)

**DAG example in airflow**

![image](https://i.ibb.co/8YNmSvg/airflow12.png)

## Dashboard
#### Dataset Overview
The dataset used for this analysis includes LinkedIn job postings from January 1, 2024, to March 31, 2024, in the United States. The dataset provides information on various job listings, including required skills, top companies, popular job roles, and hiring locations.

#### Most Hiring Locations
First, we analyzed the dataset to identify the locations with the highest number of job openings on LinkedIn. The top hiring locations in the United States during this period include (and yes, Washington DC not even in top 5):
1. New York City, NY
2. Houston, TX
3. Chicago, IL
4. Los Angeles, CA
5. Atlanta, GA

![image](https://i.ibb.co/fYddFVS/location.png)
I leave the link [here](https://lookerstudio.google.com/reporting/ebd11b86-ba9c-49a7-967b-0419a3f0975a), so you could check my report.

#### Work type preferences

![image](https://i.ibb.co/x7kczWq/work-type.png)
This overwhelming preference for onsite work highlights the prevailing traditional work culture prevalent in the job market, where physical presence in a specified location is considered the standard mode of operation. The dominant focus on onsite roles signals a strong commitment to in-person collaboration, team interaction, and face-to-face communication among organizations seeking to fill job vacancies.

On the other hand, the limited representation of remote and hybrid work setups suggests that opportunities for telecommuting or flexible work arrangements remain relatively scarce in the current job landscape. Despite the growing trend towards remote work adoption in various industries, the data from LinkedIn indicates that remote and hybrid roles constitute a minor portion of the overall job opportunities listed on the platform.

#### Top Companies on LinkedIn and
In terms of the companies that posted the most job listings on LinkedIn during the specified period, some of the top companies include:
1. TravelNurseSource
2. PracticeLink
3. Energy Jobline
4. Gotham Enterpises LTD
5. ClearanceJobs
6. McDonald's

![image](https://i.ibb.co/8D93Y1q/company.png)







## Conclusion
In conclusion, our analysis of job trends on LinkedIn provides valuable insights into the current demand for job-seekers and the skills required to succeed in this field. By understanding these trends, job seekers can better position themselves for success in their job search. Our study serves as a valuable resource for both job seekers and employers looking to navigate the competitive job market on LinkedIn.
The analysis sheds light on the prevailing work models in the job market, showcasing the dominance of onsite roles while also hinting at the entertenance of a shifting landscape towards remote and hybrid work setups. Understanding and adapting to these trends can equip stakeholders with the insights needed to navigate the job market effectively and align their strategies with the evolving dynamics of work arrangements.

## Reproduce

You can use a free version Google Cloud (upto EUR 300 credits). 

1. Create an account with your Google email ID 
2. Setup your first [project](https://console.cloud.google.com/) if you haven't already
    * eg. "YourProject", and note down the "Project ID" (we'll use this later when deploying infra with TF)
3. Setup [service account & authentication](https://cloud.google.com/docs/authentication/getting-started) for this project
    * Grant `Viewer` role to begin with.
    * Download service-account-keys (.json) for auth.
4. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
5. Set environment variable to point to your downloaded GCP keys:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys/creds>.json"
   
   # Refresh token/session, and verify authentication
   gcloud auth application-default login
 
6. Your creds.json file supposed to be in Terraform folder
My project structure:
![image](https://i.ibb.co/TcjM5V5/tree.png)
   
#### Setup for Access
 
1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
   * Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
   * Click the *Edit principal* icon for your service account.
   * Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin**
   
2. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
   
3. Please ensure `GOOGLE_APPLICATION_CREDENTIALS` env-var is set.
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   ```
#### Terraform

[Install](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) terraform on your local machine.
Fill in the variables.tf file with the necessary variables for creating BigQuery dataset and GCS Bucket.
You can use my own names, don't forget to change your project-id.

**Execution**

```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan
```

```shell
# Create new infra
terraform apply
```

```shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```
#### Run dag

Our workflow:
**format to .parquet using pandas -> to GCS -> connect GCS using pyspark > transform data using pyspark -> transfer data from spark local cluster to BigQuery**

**Dataset**
We will be using the dataset from [kaggle.com](https://www.kaggle.com/code/davedarshan/1-3-m-linkedin-job-posting-analysis), tables linkedin_job_postings and job_skills. Please download the CSV files to the airflow folder before proceeding, total size exceeding 1GB.

**Airflow**
Install `apache-airflow` with some libraries contraints that compatible with `AIRFLOW_VERSION` and `PYTHON_VERSION` to prevent any system break because of incompatibility
   ```bash
AIRFLOW_VERSION=2.9.0
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[async,postgres,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
   ```
Run `export AIRFLOW_HOME=$(pwd)` to set `AIRFLOW_HOME` variable to your current directory, but this is optional. The default value is `AIRFLOW_HOME=~/airflow` 
Run `airflow db init` to initialize SQLite Database which stores Airflow metadata based on your `AIRFLOW_HOME` variable
Create user account by running
   ```bash
   AIRFLOW_USERNAME=admin
   AIRFLOW_FIRSTNAME=John
   AIRFLOW_LASTNAME=Doe
   AIRFLOW_EMAIL=johndoe@company.org

   airflow users create \
    --username "${AIRFLOW_USERNAME}" \
    --firstname "${AIRFLOW_FIRSTNAME}" \
    --lastname "${AIRFLOW_LASTNAME}" \
    --role Admin \
    --email "${AIRFLOW_EMAIL}"
   ```
Run airflow using airflow standalone command
   ```bash
   airflow standalone
   ```
**PySpark**
To run PySpark, we first need to add it to `PYTHONPATH`:

```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH"
```

Make sure that the version under `${SPARK_HOME}/python/lib/` matches the filename of py4j or you will
encounter `ModuleNotFoundError: No module named 'py4j'` while executing `import pyspark`.

For example, if the file under `${SPARK_HOME}/python/lib/` is `py4j-0.10.9.3-src.zip`, then the
`export PYTHONPATH` statement above should be changed to

```bash
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.3-src.zip:$PYTHONPATH"
```

Download gcs-connector-hadoop3-latest.jar from [here](https://cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage) and spark-3.5-bigquery-0.37.0.jar from  [here](https://github.com/GoogleCloudDataproc/spark-bigquery-connector/releases).
These jars are necessary for us to connect and retrieve data from GCS and send it to BigQuery.

Before running your first DAG, make sure to change the variable values in the airflow/linkedin_analysis_dag.py **(dataset name and path for both files, project_id an bucket)** file and scripts/spark_transform_to_bigquery.py **(SPARK_GCS_JAR, SPARK_BQ_JAR, path to creds, path to .parquet files)** file to your own. Don't forget to answer the following two potential questions at the end of this message.