# EasyScheduler
Easy Scheduler with Django and MySQL

Steps to run locally: 
1. Install XAMPP for mysql server: https://www.apachefriends.org/. Install, open and run apache and MySQL server. 
2. You should be able to access MySQL server with this link http://localhost/phpmyadmin/index.php. Here select import option and use the SQL file included with the repo to import the db.
3. Install python in your local machine. https://www.python.org/downloads/
4. Now we have to install pip 
5. Clone EasyScheduler into into your local machine. Run the below two commands.
6. `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
7. `python3 get-pip.py`
8. Now we have to import the dependencies to run the application starting with Django.
9. `pip install django`
10. `pip install pymysql`
11. `pip install mysql-connector-python-rf`
12. `pip3 install icalendar`
13. Verify you have all dependencies by going to the project dir and running `python manage.py runserver`. If you have all the dependencies it should run the project with the below message.
14. `Django version 5.0.1, using settings 'app.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.`
15. Now you can access the application in your browser with the displayed link. 
