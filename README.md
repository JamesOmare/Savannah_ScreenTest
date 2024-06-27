# CaseLoad Management 1.0

A brief description of This project(will be updating it from time to time).

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Project Structure](#project-structure)
<!-- - [Usage](#usage) -->
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Getting Started
Before you begin, make sure you have the following installed on your system:

- Python 3.6 or higher
- pip (Python package manager)
- Virtual environment (optional but recommended) 

### Prerequisites

Knowledge And/Or Curiosity in Python.

### Installation

Provide step-by-step instructions on how to install and set up your project.

```bash
# Clone the repository
git clone https://github.com/JamesOmare/Casefile_Management.git

# Change into the project directory
cd Casefile_Management

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser (if applicable)
python manage.py createsuperuser

# Run the development server
python manage.py runserver

```

### Create a .env file in your root directory and add the following variables
  
  ```bash
EMAIL_HOST_USER=bluescrubs254@gmail.com
EMAIL_HOST_PASSWORD=ccvyrlfndfyonxdf
SECRET_KEY="your secret key here" 
DEBUG=True
  ```



## Project Structure

This is how the project structure should look like after running the above command.

Suppose you have an app called "authentication" in your project, the structure should look like this

The settings.py file contains our application configuration and tells Django which apps are installed, among other things.



```bash
your_project/
|-- your_app("authentication" in our case)/
|   |-- migrations/
|   |-- static/
|   |-- templates/
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- tests.py
|   |-- views.py
|-- your_project("core" in our case)/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   |-- wsgi.py
|-- manage.py
|-- requirements.txt
|-- .env
|-- README.md

```
<!-- ## Usage

Will Update this later. -->

## Features

These are the features which we will be adding to the project Backend API and Functionality

### Case Management
- Allow lawyers to create, edit, and manage case files, including relevant details like case information(need more research on content of cases), client information, deadlines, and associated documents.
- Enable assignment of cases to specific lawyers or teams.
- Track the progress of cases.

### Client Management
- Create and manage client profiles, Maintain a database of clients with their contact information, case history, and notes.
- Track client interactions
- (Optional) - Provide a portal where clients can view case progress, submit documents, and communicate with their lawyer.

### Document Management
- Store and organize all case-related documents
- Create and edit legal documents
- Allow easy sharing of documents with clients and other parties involved in the case.

### Communication and Collaboration:
- Facilitate communication within the legal team through an internal messaging
system.
- Record and organize communication with clients, including emails, calls, and
meetings.

### Billing and Invoicing:
- Generate invoices based on predefined billing rates, track payment status, and
send reminders for unpaid invoices.

### Task and Deadline Tracking:
- Create and assign tasks related to each case, with due dates and priority levels
- Send notifications and reminders for upcoming deadlines and important dates.

### Reports and Analytics:
- Generate reports on the progress of each case, showing completed and pending
tasks, upcoming deadlines, and other key metrics.
- Provide insights into lawyer productivity, case outcomes, and other performance
indicators.


# License

Free License.

# Acknowledgements

Will Update this later.