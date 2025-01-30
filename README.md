# Proposed solution for Data Engineer Indicium Tech Code Challenge.  

<p align="justify">In short, the challenge was to build a pipeline that extracts the data everyday from both sources and write the data first to local disk, and second to a PostgreSQL database. There were a number of requirements that needed to be followed, and you can see them in this link.(https://github.com/STEFANOVIVAS/indicium-code-challenge/blob/main/Indicium-challenge.md). You need to use some pre-defined tools like, postgres database for storage and apache airflow to schedule the pipeline, but were free to choose between Meltano or Embulk as a data loader. I chose Meltano because I feel more comfortable working with the Python language, despite knowing a little bit of Java.</p>
<p align="justify">The meltano oficial documentation provide us with some possibilities to install the tool, like pip, pipx and docker (https://meltano.com/). I ended up choosing pipx option to install meltano as a easy way to do it for a proof of concept or something. For production grade application I recommend deploy meltano with a docker container image, simplifying the process and prevent issues caused by inconsistencies between environments. In doing so, we would need to make some small changes, such as extending the Docker file to add the Meltano and Airflow services, and making some small modifications to the commands to run the application.</p>
<p align="justify"> For destination database i  extended the original docker file provided by indicium, adding another Postgres database, along with pg admin as a DBMS to interact better with data.</p>

## Prepare environment

  -  Create and navigate to a directory to hold your Meltano projects:
    
          mkdir your-project-folder
          cd your-project-folder
     
  -  Clone this repository:
    
          git clone git@github.com:STEFANOVIVAS/indicium-code-challenge.git   
          cd indicium-code-challenge
  -  Install the pipx package manager:

          python3 -m pip install --user pipx
        
  -  Install meltano package:

          pipx install meltano  
  -  Lift up source and destination databases with docker compose file:
    
          docker compose up -d

## Adding plugins to extract and load data:
<p align="justify">For load and extract data in meltano, we need to specify the type of extractor and loader we are dealing with, as the data transfer occurs from a declarative way from specifications held in the meltano.yml config file. To extract the data I chose the tap-csv and tap-postgres packages, considering that they are the source formats.To load data in the local filesystem, I chose the Comma Separated Values(csv) format and the target-csv package (meltanolabs variant), because it has an important feature for our pipeline called file_naming_scheme ({stream_name}- {datestamp}- {timestamp}.csv). It provides a way to write different streams to separate files, such as data sent from different tables in the Northwind postgres database, as an important requirement described in the project challenge.</p>
You could install all the packages required for load and extract data with the code below.
     meltano add extractor tap-csv tap-postgres  
     meltano add loader target-csv target-postgres  

## Running jobs:
You could run the entire pipeline (Extract and load) with this code...

    meltano run pipeline-csv-and-postgres-to-local-target-postgres

...or you could run each of the two steps separately...

    meltano run postgres-to-local 
    meltano run orders-details-csv-to-local  
    meltano run local-csv-to-postgres

## Passing parameters to jobs:
You could pass a DATE parameter to the job running so it will write the data locally with this parameter inside the file path such as:

    /output/postgres/{table}/DATE/file.format
    /output/postgres/{table}/DATE/file.format
    /output/csv/DATE/file.format

So, in addition to separating the data by date, we can backfill the data to a past date.  

    DATE=2025-01-01 meltano run pipeline-csv-and-postgres-to-local-target-postgres
    
## Orchestrate Data
Most data pipelines aren't run just once, but over and over again, to make sure additions and changes in the source eventually make their way to the destination.
To help you realize this, Meltano supports scheduled pipelines that can be orchestrated using Apache Airflow.

    meltano add utility airflow
    meltano invoke airflow:initialize
    meltano invoke airflow users create -u admin@localhost -p password --role Admin -e admin@localhost -f admin -l admin

Starting the Airflow scheduler

    meltano invoke airflow scheduler -D

Using Airflow directly

    meltano invoke airflow webserver -D

The web interface and DAG overview will be available at http://localhost:8080.
When accessing the web server in your browser, you must enter the username and password created in the first step of the orchestrate data section and see something like this:

![](https://github.com/STEFANOVIVAS/indicium-code-challenge/blob/main/Meltano-Airflow-webserver.png)
The first DAG is created automatically by airflow when we create a schedule in meltano.
The second DAG (northwind_meltano_pipeline) was created manually after installing airflow. This task uses the BashOperator to trigger daily jobs created on the Meltano platform, passing the actual date captured from the system as a parameter. (DATE=$(date +%Y-%m-%d).The DAGS were in the './orchestrate/airflow/dags' folder.

![](https://github.com/STEFANOVIVAS/indicium-code-challenge/blob/main/meltano-airflow-task.png)

## Accessing data loaded in the Postgres database
According to our docker-compose image, pg admin can be accessed through port 16543, therefore, if we enter the address http://localhost:16543/ we will have access to the main page of the database manager. Enter the username and password listed in the docker image (pg-admin).
In the main page you will need to add a new server. 
Choose a name to put on the server through the General tab.  
In the tab "Connection" fill in the fields HOST,PORT, DATABASE, USERNAME,PASSWORD as it is in the docker image (warehouse_db) and save it. 

<br>

![](https://github.com/STEFANOVIVAS/indicium-code-challenge/blob/main/meltano-pgadmin-server.png)  

Go to the ecommerce database, ecommerce schema and search for the tables.  
<br>
![](https://github.com/STEFANOVIVAS/indicium-code-challenge/blob/main/meltano-pgadmin-query.png)  



