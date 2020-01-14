# Personal Portfolio project
My personal portfolio and Blog project developed using Python, Flask, HTML, CSS, JS, Bootstrap and PosgreSql.



## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Note

The model is is configured for production server. To run it on development server/localhost you need to change some codes mentioned below.

##### In wsgi.py

```
from app import app
app.run(debug = True)
```

##### In conf.py

```
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
```

##### To generate database file from model

```
python

>>> from app import db
>>> db.create_all()
>> exit()
```

### 1. Clone the repository

```
git clone https://github.com/joshy-joy/portfolio.git
```

### 2. Create a python 3 virtual environment using 'virtualenv'

```
pip install virtualenv

virtualenv -p python3 venv

source venv/bin/activate
```

### 3. Install the requirements using requirements.txt

```
pip install -r requirements.txt
```

### 4. Run the project

```
python wsgi.py
```


## Authors

* **Joshy Joy** - *Initial work* - [Joshy Joy](https://github.com/joshy-joy/)
