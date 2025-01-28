# Proposed solution for Data Engineer Indicium Tech Code Challenge.  
The challenge specifications can be found at [this link.](https://github.com/STEFANOVIVAS/indicium-code-challenge/blob/main/README.md)
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

