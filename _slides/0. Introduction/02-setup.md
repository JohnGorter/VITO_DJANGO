# Setup

---
### Getting started

What you need:
- Python
- Virtualenv
- Django

Using virtual environments is not mandatory, but it’s highly recommended


---
### Install Python3
To install Python 3 on a MAC, run the command below
```
brew install python3
```

Since macOS ships with Python 2, after you install Python 3, you will have both versions

To run Python 2, use the python command in the Terminal. For Python 3, use python3 instead

Windows users navigate to http://www.python.org and click on the Python download page

---
### Test Python3

We can test the installation by typing in the Terminal:
```
python3 --version
```

---
### Virtualenv

For MAC users, in the Terminal, execute the command below:
```
sudo pip3 install virtualenv
```

So far the installations that we performed was system-wide. From now on, everything we install, including Django itself, will be installed inside a Virtual Environment

---
### Next steps
- create a folder named Development (use to organize all projects and websites)
- creating a new folder with the project name inside Development folder
```
mkdir myproject cd myproject
```
- create a virtual environment
    - inside the myproject folder
```    
virtualenv venv -p python3 
```
- use the virtual environment
```
source venv/bin/activate
```
- install DJANGO
```
pip install django
```


---
### Summary
- We created a special folder named venv
- It contains a copy of Python inside this folder
- After we activated the venv environment, when we run the python command
    - it will use our local copy, stored inside venv, instead of the other one we installed earlier

Note that when we have the venv activated, we will use the command python (instead of python3) to refer to Python 3.6.2, and just pip (instead of pip3) to install packages.

---
### Create our first project
To start a new Django project, run the command below:
```
django-admin startproject myproject
```

Right now, our myproject directory looks like this:
```js
myproject/          <-- higher level folder
|-- myproject/      <-- django project folder
| |-- myproject/
| | |-- __init__.py
| | |-- settings.py 
| | |-- urls.py
| | |-- wsgi.py
| +-- manage.py 
+-- venv/           <-- virtual environment folder
```

---
### The files 
- manage.py: a shortcut to use the django-admin command-line utility
    - it’s used to run management commands related to our project
    - run the development server, run tests, create migrations and much more
- \_\_init\_\_.py: this empty file tells Python that this folder is a Python package
- settings.py: this file contains all the project’s configuration. We will refer to this file all the time!
- urls.py: this file is responsible for mapping the routes and paths in our project
- wsgi.py: this file is a simple gateway interface used for deployment. You don’t have to bother about it. Just let it be for now

---
### Run the first project
We can test our project by executing the command
```
python manage.py runserver
```
Open the URL in a Web browser: http://127.0.0.1:8000



---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Installing and using DJANGO

---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Installing and using DJANGO



