# Django Todo

This is a Django project that includes instructions on how to set up and run the project locally.

## Clone the Repository

To get started, clone this GitHub repository to your local machine using the following command:


git clone https://github.com/lklivingstone/algobulls-assignment.git

Set Up a Virtual Environment
It is recommended to use a virtual environment to isolate the project's dependencies. Follow these steps to create and activate a virtual environment:

Change into the project directory:

```
cd your-project
```

Create a virtual environment using venv or virtualenv. Run one of the following commands:

For venv (Python 3):
```
python3 -m venv env
```
For virtualenv:
```
virtualenv env
```
Activate the virtual environment:

On macOS/Linux:
```
source env/bin/activate
```
On Windows:
```
.\env\Scripts\activate
```
Install Dependencies

Once the virtual environment is activated, install the project dependencies using pip:
```
pip install -r requirements.txt
```
Apply Migrations

Before running the project, apply the database migrations using the following command:
```
python manage.py makemigrations
python manage.py migrate
```
This will create the necessary database tables based on the project's models.

Run the Development Server

Finally, start the Django development server to run the project locally:
```
python manage.py runserver
```
The development server should start running at http://127.0.0.1:8000/

That's it! You can now access the Django project in your web browser and begin development or testing.

## Coverage Report

### Unit Tests
![Screenshot (188)](https://github.com/lklivingstone/algobulls-assignment/assets/74340009/5629049e-e487-4552-8145-74c51c3c6d19)


### Selenium Tests
![Screenshot (189)](https://github.com/lklivingstone/algobulls-assignment/assets/74340009/2772baee-0109-4de0-94eb-103c65bef9a3)


## Github Workflow Actions

Checkout Code:
Uses the actions/checkout used to fetch the repository's code.


Set up Python:
Uses the actions/setup-python action to set up a Python environment with version 3.11.0.


Install Dependencies:
Upgrades pip and installs the Python dependencies from requirements.txt file.


Set up Node.js:
Uses the actions/setup-node action to set up Node.js with version 14. (Used for selenium tests)


Set up Chrome:
Uses the browser-actions/setup-chrome action to set up the Chrome browser.  (Used for selenium tests)


### Upload coverage report
Uses actions/upload-artifact@v2 for uploading artifacts.
The path is the path of the directory or file that is to be uploaded as an artifact. Here, it's the directory containing the HTML coverage report generated during tests.


### Tests:

```
python manage.py runserver 8000 &
sleep 10
coverage run manage.py test task
coverage html -d coverage_html_unit
```


```
python manage.py runserver 8000 &
sleep 10
coverage run manage.py test tests.test_admin_view.AdminTests
coverage html -d coverage_html_selenium
```


Run Server:
Executes commands to run the Django development server in the background (python manage.py runserver 8000 &).
Pauses for 10 seconds to allow the server to start (sleep 10).
Runs unit tests for the task app using the command coverage run manage.py test task and stores the coverage for it.
Runs Selenium tests for the tests.test_admin_view.AdminTests class using the command coverage run manage.py test tests.test_admin_view.AdminTests and stores the coverage for it.
Saves the html file of the coverage using the command coverage html -d <html_file_name>




### Lint:

```
flake8
```
Run Flake8:
Executes the flake8 command to perform linting checks on the Python code.


```
black --check .
```


Run Black:
Executes the black --check . command to perform a check for code formatting violations. The --check option checks for formatting issues without modifying the code.


### Black check for Main Branch PRs:


```
black --check .
```


Trigger: 
Runs on every pull request that targets the main branch.

### Black check for PR on Delta Changes


```
if git diff --name-only ${{ github.event.before }} ${{ github.sha }} | grep -q '\.py$'; then
    git diff --name-only ${{ github.event.before }} ${{ github.sha }} | grep '\.py$' | xargs black --check
else
    black --check .
fi
```


Trigger:
Runs on every pull request to any branch.

It checks whether there are any changes in files with a ".py" extension between the commit represented by ${{ github.event.before }} and the current commit represented by ${{ github.sha }}.
It performs a Git diff operation to obtain the names of the files that have changed between the two commits.
It runs Black (black --check) only on the changed Python files.
The xargs command is used to pass the file names as arguments to the Black command.

If there are no git commit before the current commit, it runs Black (black --check) on the entire codebase (all files).


## Tests upon PR:
### PR to Main branch

#### 6 Tests


![Screenshot (196)](https://github.com/lklivingstone/django-tests/assets/74340009/85367752-e77c-4a6a-b837-8746a50b46da)



### PR to other branches


#### 5 Tests

##### Success

![Screenshot (198)](https://github.com/lklivingstone/django-tests/assets/74340009/5c855102-4df2-4458-aa57-bf5ed41851eb)

##### Failure

![Screenshot (199)](https://github.com/lklivingstone/django-tests/assets/74340009/2970c5da-6cb7-4bf8-89a1-814f8e5a9aac)



### Artifacts for Downloading Coverage Report

![Screenshot (197)](https://github.com/lklivingstone/django-tests/assets/74340009/f843c48d-61a4-4859-8e64-36c77c3116e5)

