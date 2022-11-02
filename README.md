1. set up python virtual environment (creating a folder 'venv' within 'backend/py', copy contents from the venv library of python37)
PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ cd backend/py
PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ py -m venv venv

Note: seems work to copy the venv from the python37 library -- no need to use install virtualenv

2. activate the virtual env (venv)
PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ Set-ExecutionPolicy Unrestricted -Scope Process
PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ venv\Scripts\activate

3. upgrade the pip command (upgrade the pip within the venv), and add the folder 'backend/py/venv/' and '__pycache__/' into gitignore list
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ python -m pip install --upgrade pip

4. install python libraries

- Flask and flask-restful
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ pip install Flask
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ pip install flask-restful

- dotenv ( to read and set python environment variables )
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ pip install python-dotenv

- setuptools wheel
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ pip install -U pip setuptools wheel

- spacy
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ pip install spacy
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ python -m spacy download en_core_web_sm

-cors (allowing visitng sites acrossing domains, -- when visiting the Python API in a different domain)
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ pip install flask-cors

- also benpar?

(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1\backend\py> $ pip install gunicorn 

5. add data, frontend index.html, js apps, backend py modules (as show in the folder)

6. In Start Command, enter the following line:
```
gunicorn --chdir backend/py/test01 __init__:appFlask
```


7. make a requirement.txt (so as to tell render site to load the required packages)
(venv) PS C:\Users\syao2\AppData\Local\MyWorks\js\rendertest1>$ pip freeze > requirements.txt
The file is created in /backend/py/ as it is the location where python starts. 
Move the file to the project root folder. 

visit https://rendertest1.onrender.com (need to wait for a while as it need to be waken up)
This project only works on line and on VCH machine (in yoga 7 the packages are not installed ...)
The app is in test01