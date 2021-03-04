# trello-app

## To setup

1. ```git clone https://github.com/mvyuson/trello-app.git```
2. ```cd trello-app```
3. ```python -m venv venv```
4. ```venv\Scripts\activate```
5. ```pip install -r requirements.txt```
6. ```cd trello/static```
7. ```npm install```
8. Download jquery-ui-1.12.1.custom.git from [jqueryui site](https://jqueryui.com/) or clone from [jqueryui repo](https://github.com/mvyuson/jquery-ui-1.12.1.custom.git) and store it inside the node_modules. Please use this version because **sortable** and **draggable** features does not work well in other versions.
9. Go back to trello-app directory
10. ```python manage.py migrate```
11. ```python manage.py runserver```

#### Go to localhost:8000/


## Preview of the app

![login](https://user-images.githubusercontent.com/32087081/110012008-038cff00-7d5b-11eb-8019-576c308a3b25.PNG)

![boards](https://user-images.githubusercontent.com/32087081/110012019-07b91c80-7d5b-11eb-9920-4246c007804f.PNG)

![board](https://user-images.githubusercontent.com/32087081/110012066-143d7500-7d5b-11eb-827e-e87397472e12.PNG)
