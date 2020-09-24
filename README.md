# Saver Life Budgeting App


## Install
Set up Python virtual environment with Python 3.6 or later. 
In the virtual environment install:
- Django 3.1
- psycopg2 2.8.5
- holidays 0.10.3

Install 
- PostgreSQL 

Set up database budgetingapp and database user with all privleges. 

See the set-up.sql in the the db_resources directory. 

You may need to update the settings.py in the budgetingapp directory to reflect any deviations in your database setup. 

Note that it is important the database user have the ability to create databases for testing purposes. 

To intialize the application database. 
```
>python manage.py makemigrations users
>python manage.py migrate
>python manage.py makemigrations
>python manage.py migrate
```
This sets up the intial necessary database. 

To run the server:
```
>python manage.py runserver
```

## Remaining Steps:
- Add much more additional testing 
- Add delete functionality on Accounts, Income, Expenses
- Add better support for serving up static files
- Take note of sections with TODO labels 

## Additional Notes/Explanation: 
- The models Budget to Accounts and Incomes to Accounts should allow users to indicate how a budget/income source might be split among different accounts
- The model Account Entries should be used to track historic changes to the accounts
 
