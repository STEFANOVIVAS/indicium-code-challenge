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

## Adding Extractors to Pull Data from Sources
