# Check Service

API service for handling checks, creating PDF files for checks also printing check

# Installing using GitHub

```shell

git clone https://github.com/AntonShpakovych/sheep-fish-task
#
cd sheep-fish-task
#
python -m venv venv (for Windows)
#
venv\Scrpits\activate (for Windows)
#
pip install -r requirements.txt
#
create .env file based on .env.sample
#
docker compose up --build
#
python manage.py migrate
#
python loaddata fixtures/point_printer_fixture.json
#
celery -A config worker -l info
```


#### DOCUMENTATION - api/v1/doc/swagger/
