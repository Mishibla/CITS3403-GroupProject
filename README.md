# CITS3403-GroupProject
1)A description of the purpose of the application, explaining the its design and use.
The purpose of the application is to create a request forum application, specifically allow users to make and answer requests. The application allows users to buy and sell variety of online game accounts such as Valorant, Overwatch, CSGO & League of Legends. The users can submit a request to sell an existing account to the public or browse through the webpage using the filters which will satisfy the needs. The creation of the application to allow online players of the aforementioned game platforms to conviently start playing competitive matches without the need of investing time and effort to meet the required benchmark for competitive modes. 
2)A table with with each row containing the i) UWA ID ii) name and iii) Github user name of the group members.
UWA_ID      name                Github_username
23639794    Matthew Loo         PeanutJam5255    
23640682    Christoper Jongue   Mishibla 
23994848    Jonathan Clyde      Jonno421 
22444784    Amir Afiq Hassani   afiqhassani 
3)A brief summary of the architecture of the application.
Our project was formed using common architecture for web design this included CSS, HTML, Javascript and python with these together with SQlite we created a flask environment for hosting the various forms of architecture used and for demonstrating our abilities with them. 
Frontend:
-	HTML provided the structure of our webpages to create an easy to handle user interface
-	CSS provide styling of the HTML elements to make them visual appealing 
-	Javascript gave the webpages interactivity and added a dynamic behaviour to the user interface
Backend:
-	Python served as our backend programming language, using it to process requests from the frontend and execute logic within our framework
-	Our framework of choice was flask and we used this to build our backend server and show off the frontend UI
-	Flask integrates with Jinja2 which allowed us to generate dynamic HTML content 
Database
-	We made use of SQLAlchemy to create a database instance that interacts with our applications database
-	Set up folder configurations for storing images
-	Importing models for use with our database models using SQLAlchemy

4)Instructions for how to launch the application.
Read requirements.txt to know which modules are required for our application
ensure you have opened a wsl terminal 
enter export GROUP_PROJECT_SECRET_KEY='cats' in the wsl terminal 
enter export FLASK_APP=project.py in the wsl terminal
enter flask run in the wsl terminal 
cntrl click on the server URL to see the homepage

5)Instructions for how to run the tests for the application.
