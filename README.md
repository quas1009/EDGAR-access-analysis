# Geologation
> ***Real-time dashboard for log analysis***

NY-20A Insight data engineering project.
Website link: [dataengineer.cc] (http://dataengineer.cc/)

***

## Introduction

*Real-time module:* The webapp displays where clicking activities are happening all over the world; high frequncy ip clicking activities and their frequencies.
*Historical module:*
Also, it analyzes the document accessed activities of each company from the EDGAR log files to heatmap the website users’ attention on the current primary business on the web app. A kafka->spark streaming pipeline is used to process tons of log file data. My product aims to give recommendations on which location should the company open a new branch. 

![](./images/webapp.png)
header and box style reference: Apache Echarts Plaftorm Template

## Pipeline
![](./images/pipeline.png)

## File Structure
```
.
├── README.md
├── app
│   ├── server.py
|   ├── static
|   |   ├── css
|   |   |   └── app.css
|   |   ├── js
|   |   |   ├── map-usa.js
|   |   |   └── map-world.js
|   |   └── img
|   |       ├── bg01.png
|   |       ├── header.png
|   |       └── panel.png
|   |
│   └── templates
│       └── index.html
├── images
│   ├── pipeline.png
│   └── webapp.png
|
├── kafka
│   ├── kproducer.sh
│   └── kproducer.py
|
├── stream
│   └── stream.py
|
├── data
|   ├── fetchdata.py
|   ├── iplist
|   └── sample.txt
|
├── requirements.txt
└── sql_schema.txt
```

## Setup
Install and configure [AWS CLI](https://aws.amazon.com/cli/) and [Pegasus](https://github.com/InsightDataScience/pegasus) on your local machine. Setup 4 `m4.large` EC2 instance and install awscli.

```bash
$ pip install awscli
```
Add the following credentials as environment variables to your `~/.bash_profile`.

```bash
# AWS Credentials
export AWS_BUCKET_NAME=XXXX
export AWS_ACCESS_KEY_ID=XXXX
export AWS_SECRET_ACCESS_KEY=XXXX

# PostgreSQL configuration
export POSTGRESQL_USER=XXXX
export POSTGRESQL_PASSWORD=XXXX
export POSTGRESQL_HOST_IP=XXXX
export POSTGRESQL_PORT=XXXX
export POSTGRESQL_DATABASE=XXXX

# Upgrade Spark default python version to 3.7
export PYSPARK_PYTHON=XXXX
export PYSPARK_DRIVER_PYTHON=XXXX
```
