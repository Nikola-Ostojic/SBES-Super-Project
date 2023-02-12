# Safety and Security Project

Project created for a class in the Faculty of Technical Sciences. 

## Table of Contents
* [General](#general)
* [Technologies](#technologies)
* [Run](#run)
* [Summary](#summary)
* [Team Members](#team-members)

## General

Goal of this project was to build a questionnare system that will calculate the amount of money needed for an IT company to hire an assurance company for the given
infrastructure in place according to the research paper 'Određivanje cene sajber osiguranja za mala i srednja preduzeća' by MsC Jelena Sekulić. The application consists from two major endpoints which are "/" and "/admin". Starting route sends users directly to the questionnare and after
it is filled correctly they are given the price per year to use assurance. The result page gives comprehensive data for the user to understand how the value is being calculated,
while keeping the secrets behind the exact way the amount is being calculated keeping the business secret. The way questionare works is by using a JSON configuration file.
The configuration file keeps the lists of all pages, questions and answers with all of their details from which all the data that is shown to user is read. The administartion
page uses a dropdown menu where the user can select the any of the questionnaire based objects and edit their properties like text, order and others.

## Technologies
* Python
* Flask 
* MySQL
* HTML, CSS, JS

## Run
1. Use git to pull the whole repository `git clone https://github.com/AleksaBajat/SBES-Team-Project.git`
2. Open terminal inside the root folder and run `python main.py`


## Summary

There are some improvements that could be made to make the experience even better:
1. Making the pages responsive (mobile ready)
2. Configuration file should be extended to support multiple questionnaires
3. There should be an authentication/authorisation layer to enter the admin page
4. Argument could be made that configuration should be kept in the database as well
5. Application should be dockerised in order to support easy deployments and usage of environment variables and secret keys
6. Flask by itself is not production ready and WSGI should be used
7. Adding schema.org and SEO optimisations

Software development is a continuous process and almost certainly after implementing all of these improvements there would be always something more to add or improve,
and the effort that should be put into it should be based on the amount of users that are accessing and using the application.


## Team members
    Dragan Stančević
    Aleksa Bajat
