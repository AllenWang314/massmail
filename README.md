# massmail
Tool that sends mass custom emails

## Structure

```
|
\-- config.txt          template for constants
\-- constants.py        constants including email body
\-- email.py            script entry point
\-- README.md           this document

```

## Setup

1. To setup the application, you will need python 3, pip, and virtualenv. You can run the application without pip or virtualenv if pandas is already installed.

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

2. Next make sure that data.csv is filled out. Currently it contains a sample of what such a csv can look like. The first row of the csv should contain the column names that will be substituted in the body and subject line of the emails. Make sure that one of the columns is called "email" as it is required.

3. Finally replace constants.py with the appropriate email and subject line like how the template currently does it using an f-string.

## Usage

To run simply run one of the commands

- ```python massmail.py -s``` prints 3 sample emails that will be sent to the console
- ```python massmail.py -t``` sends 3 test emails to your email address
- ```python massmail.py``` sends emails to all recepients

