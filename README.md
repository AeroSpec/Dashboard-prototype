# AeroSpec Environmental Quality Monitoring Dashboard

### Sponsor: Sep Makhsous, AeroSpec
### Authors: Sam Miller, Sreeja Vishaly, Bianca Zlavog
### University of Washington, MSDS Capstone Project 2021


#### Project summary
[AeroSpec](https://www.aerospec.io/) is a UW-based startup which designs and calibrates sensors to measure local air quality, noise, temperature, and other environmental data in real time. This product allows users in commercial and industrial settings to effectively manage environmental hazards, mitigate the health impacts of these factors, and maintain the safety of their facilities. Our project goal was to create a data visualization concept and prototype for AeroSpec’s user interface. The aim was to display the data collected by sensors to users in a clear and interpretable way, leveraging effective visual design principles. We produced a visualization dashboard to be utilized in upcoming product demos and pilot studies in dental offices and manufacturing plants. 

This repository contains the code developed for this project, as well as documentation of the design process and software used.


#### Project documentation
A file describing our team's design process, software features, and references to resources used, can be found at [Project_Documentation.ipynb](Project_Documentation.ipynb). Additional project assignments and resources can be found in the relevant [Google Drive space](https://drive.google.com/drive/folders/1HXya5bPvwyZrA09tZ6vSP41jBDHc6YQh?usp=sharing).


#### How to run
To run the dashboard app locally:
* `python app.py`
* In a web browser, navigate to the link indicated in the terminal at `Dash is running on [link]`

To deploy on heroku:
* `heroku create aerospec-dashboard`
* `git push heroku main`
* `heroku ps:scale web=1`
* In a web browser, navigate to https://aerospec-dashboard.herokuapp.com
