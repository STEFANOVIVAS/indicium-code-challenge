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

## Running jobs:
To extract and load data using Meltano you need to install specific packages according to the source and destination of the data,
such as postgres, csv, parquet, etc. 
However, since the packages are already inside the Meltano configuration file (meltano.yml), just run a task or job, then the application itself will install the packages for you.  So you could run the extract and load pipeline, passing a date as an argument, to install all the packages needed for this project.

    DATE=2025-02-02 meltano run pipeline-csv-and-postgres-to-local-target-postgres
