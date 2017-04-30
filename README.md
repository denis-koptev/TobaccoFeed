## TobaccoFeed

From potential creators of porn-social network

## Description

More and more people are starting to smoke hookas. Hookas are the part of our culture.
It will be great to have unified resource with all information about tobaccos.
We will give people the opportunity to choose products according to their preferences.
Users will be able to communicate and share, to add tobaccos and find the best prices.

## How to start

Download *[Python3](https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe)*

Install with PATH and name limit deactivation

Clone project
`git clone https://github.com/denis-koptev/tobacco_project`

Setup virtual environment after python installation

It can be done from every folder, but `/django` is better
* `cmd > pip install virtualenv`
* `cmd > virtualenv env`

It will create `env` folder in current dir

For activation: `env\Scripts\activate.bat`

For deactivation: `env\Scripts\deactivate.bat`

### Continuous actions are done inside `env`:

All  dependencies are in `requirements.txt`

For dependency installation: `pip install -r requirements.txt`
	
To create this file (or update) when there are new modules installed with `pip`: `pip freeze > requirements.txt`

If there are errors try: `pip install Django` or/and `pip install Pillow`

*Note: it won't be enough in the future as far as new modules will be installed*

## Server launching

* Move into directory `tobacco_project/django/tobaccopoisk`
* Run: `manage.py runserver`
* Optionally we can specify port: ip:port
* Default: 127.0.0.1:8000

## Running on Ubuntu

* Python3 should be installed by delault
* `apt-get install git`
* `git clone https://github.com/denis-koptev/tobacco_project`
* `apt-get install python3-pip`
* `pip3 install virtualenv`
* `virtualenv env`
* `source env/bin/activate`
* `pip3 install -r requirements.txt`
* `python3 manage.py runserver`

## User creation in admin panel

* `manage.py createsuperuser`
* To enter admin panel go to `<site_domain>/admin`

## html & python interconnection (templates)

* html files placed in
(*<app_name>/templates/<app_name>*) for each application (tobacco, main, etc)

## Work with static content
Create folder for static for each application

E.g.: **/tobaccopoisk/main_page/static/main_page/** 
(*/<project_name>/<app_name>/static/<app_name>/*)

Path (to static file) example: **/tobaccopoisk/main_page/static/main_page/image.jpg** 
(*/<project_name>/<app_name>/static/<app_name>/file*)

### Setting up static

In settings.py code `STATICFILES_DIRS` object must include every application

Example for main_page : `os.path.join(BASE_DIR, "main_page/static")`
### Template usage
* `{% load static %}`
* `<img src="{% static "main_page/hookah.jpg" %}" alt="My Hookah"/>`

*More examples: https://www.djangoproject.com/*


## TO DO LIST

- [ ] Create tag handling engine
- [ ] Create engine for static paths
- [ ] Move on MySQL :star:
- [x] Start filling DB with tobaccos
- [ ] Clustering of data, Statistics, Machine Learning

## TO TEST LIST (in russian)

- [ ] Проверить, что при замене фото к табаку через админку, старое фото удаляется
- [ ] Проверить, что поле поиска работает корректно (не алгоритм поиска, а сама кнопка)
- [ ] Проверить, движок поиска. Поиском ошибок 1 рода - очень важно. Поиск ошибок 2 рода - не критичны :rocket:
- [ ] Вынести алгоритм поиска в engine :rocket:
- [ ] Удаление картинки табака при удалении его из БД
- [ ] RESTfull API для поиска
- [ ] Реализовать возможность добавлять в БД имена и бренды с пробелами и заглавными буквами