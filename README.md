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

## Managing Meltano config file
After instaling the plug-ins we need to add some fetaures to standard installation in the maltano.yml file to attend some requirementes.
- tap-postgres plug-in:
  
      Insert database northwind connection data.
      Use stream-maps Capabilities to change table names from public-categories to categories, for example.
      Use select feature to bring all tables from database (public-*.*)
- tap-csv--from-csv as an alias for the data comming from csv file:
  
      Add file config feature to provide system path, entity, primary keys and delimiter.

- tap-csv plug-in for data comming from postgres data:
  
      Add file config feature to provide system path, entity, primary keys and delimiter.
      Adding parameter $DATE to file path to capture only data for the present day, in a regular daily scheduled pipeline, or any backfiling for past day run.
      
- target-postgres plug-in:
  
      Insert database warehouse connection data.
    
- target-csv--from-postgres as an alias for the CSV files comming from postgres DB:
    
      Adding parameter $DATE to file path to write files in the local filesystem only data for the present day, in a regular daily scheduled pipeline, or any backfiling for past day run ($MELTANO_PROJECT_ROOT/output/postgres/{stream_name}/$DATE/{stream_name}.csv)
  
      Adding a replace file as an overwrite behavior to guarantee idempotent pipeline behavior in this context.
- target-csv--order-details as an alias for CSV file comming from order_details file:
  
      Adding parameter $DATE to file path to write files in the local filesystem only data for the present day, in a regular daily scheduled pipeline, or any backfiling for past day run ($MELTANO_PROJECT_ROOT/output/csv/{stream_name}/$DATE/{stream_name}.csv)
  
      Adding a replace file as an overwrite behavior to guarantee idempotent pipeline behavior in this context.
    
Things to point out:

  -  In a real backfilling pipeline, we need to pass the date inside the source to filter data only for that period.
  -  The option for default replication method may vary depending on requirements for pipelines, like full or incremental load.
## Meltano jobs
The meltano tool allows you to create a functionality called Job, which allows you to run a set of chained tasks with just one command. Considering the need to make the pipeline modular, so that we can reprocess just one of the steps, 4 jobs were built for the pipeline.

  - postgres-to-local, which represents the task that extract data from postgres (tap-postgres) and write a CSV file(target-csv--from-postgres).

  - orders-details-csv-to-local, which represents the task that extract data from CSV (tap-csv--from-csv) and write a CSV file(target-csv--order-details)

  - local-csv-to-postgres, which represents the task that extract data from all the CSV files (tap-csv) and load them into a postgres database(target-postgres)

  - pipeline-csv-and-postgres-to-local-target-postgres that executes all the pipeline at once, one step at once [tap-postgres target-csv--from-postgres tap-csv--from-csv target-csv--order-details, tap-csv target-postgres]

This way, you could run the entire pipeline (Extract and load) with this code...

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

So, in addition to separating the data by date, we can backfill the data to a past date... 

    DATE=2025-01-01 meltano run pipeline-csv-and-postgres-to-local-target-postgres

## Orchestrate Data
Most data pipelines aren't run just once, but over and over again, to make sure additions and changes in the source eventually make their way to the destination.
To help you realize this, Meltano supports scheduled pipelines that can be orchestrated using Apache Airflow. From meltano's documentation we can see how to add airflow scheduler in our project.

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
The second DAG (northwind_meltano_pipeline) was created manually after installing airflow. This task uses the BashOperator to trigger daily jobs created on the Meltano platform, passing the actual date captured from the system as a parameter (DATE=$(date +%Y-%m-%d).This way the schedule pipeline will always use the current date as a parameter and so creating folders with the day it was executed. It was created a dependency between tasks in a way that Step 2 depends on both tasks of step 1. The DAGS were stored in the './orchestrate/airflow/dags' folder.

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



