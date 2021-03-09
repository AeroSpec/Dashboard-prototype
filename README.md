# AeroSpec Environmental Quality Monitoring Dashboard

### Sponsor: Sep Makhsous, AeroSpec
### Authors: Sam Miller, Sreeja Vishaly, Bianca Zlavog
### University of Washington, MSDS Capstone Project 2021


#### Project summary
[AeroSpec](https://www.aerospec.io/) is a UW-based startup which designs and calibrates sensors to measure local air quality, noise, temperature, and other environmental data in real time. This product allows users in commercial and industrial settings to effectively manage environmental hazards, mitigate the health impacts of these factors, and maintain the safety of their facilities. Our project goal was to create a data visualization concept and prototype for AeroSpec’s user interface. The aim was to display the data collected by sensors to users in a clear and interpretable way, leveraging effective visual design principles. We produced a visualization dashboard to be utilized in upcoming product demos and pilot studies in dental offices and manufacturing plants.


#### Design process and software documentation
A document describing the design process, software features, and references to resources used, can be found at [Design_Prototypes.ipynb](https://github.com/sammiller11235/Aerospec-Data-Viz/blob/main/Design_Prototypes.ipynb).


#### How to run
To run the dashboard app locally:
* `python app.py`
* In a web browser, navigate to the link indicated in the terminal at `Dash is running on [link]`

To deploy on heroku:
* `heroku create aerospec-dashboard`
* `git push heroku main`
* `heroku ps:scale web=1`
* In a web browser, navigate to https://aerospec-dashboard.herokuapp.com
