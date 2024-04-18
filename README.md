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