# Budget App
App is designed to write and control outcomes and incomes by category or date.

___
# Features:
 - Adding and deleting expenses and incomes with category, date and description
 - Adding and deleting categories
 - Filtrating entries by amount, date and category
 - Estimating future expenses
 - Full authentication
 - Default categories for new users

___
# Work in progress:
 - possibility to analyze incomes and expenses by categories, months or amount
 - possibility to estimate future expenses and incomes displayed by months
 - possibility to compare estimated and real incomes and expenses
 - possibility to enter value of different assets and displays total actual sum (with all your incomes and expenses)

___
# Notes:
Entries in Expenses are filtered by default for the current month, but incomes, expenses and balance displays sum for all entries.

When filtering entries by date, it does not display that these entries are displayed from a specific date.

Deleting a specific category means that this category also disappears in the incomes and expenses entry.

___
# Setup

The first thing to do is to clone the repository:

[//]: # (zmienic linka do repozyttorium)
```sh
$ git clone https://github.com/gocardless/sample-django-app.git
$ cd sample-django-app
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/` in your browser.

If you want to add and see entries you need to register first.