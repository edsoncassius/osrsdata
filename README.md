# OSRS Data Project

## Introduction

This project was developed for storing player data from the Old School Runescape API into a POSTGRESQL Database. The data can be used to check the player's progression over time.

## Pipeline

### Data Extraction

Each player Hiscores Data is obtained hourly from the available OSRS API: 
E.g. https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=zezima

Data is paired with the respective names for each skill and boss kill count.

### Database Insertion and Validation

Data is validated from each user's last record in the database to check data format and if insertion is necessary.

### Retrieving Data and Visualization

Each player's data can be retrieved directly from the PostgreSQL database and sent to Tableau or any other visualization tool for creating charts to follow character development and other insights.