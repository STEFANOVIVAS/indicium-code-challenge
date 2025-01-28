# Proposed solution for Data Engineer Indicium Tech Code Challenge.  
The challenge specifications can be found at [this link.](https://github.com/STEFANOVIVAS/indicium-code-challenge/blob/main/Indicium-challenge.md)
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



