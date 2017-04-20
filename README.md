## tobacco_project

From potential creators of porn-social network


## How to start

Download python3 https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe

Install with PATH and name limit deactivation

Клоним проект
* [git clone https://github.com/denis-koptev/tobacco_project]

После установки питона нужно поставить виртуальное окружение

Можно это сделать из любой папки, но лучше в папке django рядом с папкой tobacco
* [cmd > pip install virtualenv]
* [cmd > virtualenv env]

Это создаст папку env в текущей директории

Для активации 	
* [env\Scripts\activate.bat]

Для деактивации 
* [env\Scripts\deactivate.bat]

### Далее все действия внутри окружения:

Все зависимости лежат в файле requirements.txt

Для скачивания необходимых зависимостей:
* [pip install -r requirements.txt]
	
Чтобы сделать такой файлик, допустим, при скачивании новых модулей через pip, нужно исполнить следующую команду:
* [pip freeze > requirements.txt]

Если возникнут какие-то ошибки можно попробовать:
* [pip install Django]
* [pip install Pillow]

В будующем этого может стать недостаточно, т.е могут появить еще модули!!!

## Запуск сервера

* Перейти в папку проекта tobacco_project/django/tobaccopoisk
* Выполнить: [managy.py runserver]
* Опционально: после вызова можно указать ip:port
* По дефолту: 127.0.0.1:8000

## Создание юзера в админке

* manage.py createsuperuser
* Чтобы войти, к адресу сайта приписываем /admin

## Связь html и питона (шаблоны)

* Соответсвующие html коды помещены в папку
<appname>/template/<appname> для каждого приложения (tobacco, main и т.д.)
