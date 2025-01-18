
* need to use it via /usr/bin to bypass cursor venv

- pip freeze > requirements.txt (to put current venv pacakges into requirements.txt)
- /usr/bin/python3 -m venv venv && source venv/bin/activate
- pip install --upgrade pip
- pip install -r requirements.txt
- python manage.py runserver
