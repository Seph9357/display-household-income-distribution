# national-household-income-distribution
Display the situation of State HH Income/SA4 HH Income with filter function

### Guide for launch this system

#### 1. Set up virtual environment for further development or testing

##### 1.1 install pyenv

Please see reference：https://github.com/pyenv/pyenv#installation

##### 1.2 install python-virtualenv

Please see reference：https://github.com/pyenv/pyenv-virtualenv

##### 1.3 install python with required version
```bash
pyenv install 3.8.8
```

##### 1.4 set up virtual environment for this project
> income_distribution: self-defined name of the virtual environment
```bash
pyenv virtualenv 3.8.0 income_distribution
```

##### 1.5 switch to this virtual environment
```bash
# switch to the directory of project 
cd display_household_income_distribution/
# switch to this virtual environment: income_distribution
pyenv local income_distribution
```

#### 2. Install relevant python libraries
```bash
# switch to directory of incomedistribution
cd incomedistribution/
# Install all required python libraries
pip install -r requirements.txt
```

#### 3. Run this Django project 
```bash
python manage.py runserver 8000
```

#### 4. Make migrations of data models to create new tables in database
```bash
python manage.py makemigrations
python manage.py migrate
```

