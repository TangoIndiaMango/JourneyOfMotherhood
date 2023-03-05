# JourneyOfMotherhood

## Running the program
- git clone the repo
- open your terminal/console
- create an enviroment
- If you're using bash 
### NOTE: if different please consult external sources for how to setup enviroment
```
python -m venv .venv
```
- activate your enviroment
```
source .venv/Scripts/activate
```
- run 
```
pip -r requirements.txt
```
- migrate the databse
```
python manage.py makemigrations
python manage.py migrate
```
- Run the server
```
python manage.py runserver
```
- Use the postman collection to understand the endpoints available
