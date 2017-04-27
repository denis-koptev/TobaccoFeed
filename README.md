## TobaccoFeed

From potential creators of porn-social network

## Description

More and more people are starting to smoke hookas. Hookas are the part of our culture.
It will be great to have unified resource with all information about tobaccos.
We will give people the opportunity to choose products according to their preferences.
Users will be able to communicate and share, to add tobaccos and find the best prices.

## How to start

Download python3 https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe

Install with PATH and name limit deactivation

Клоним проект
`git clone https://github.com/denis-koptev/tobacco_project`

После установки питона нужно поставить виртуальное окружение

Можно это сделать из любой папки, но лучше в папке django рядом с папкой tobaccopoisk
* `cmd > pip install virtualenv`
* `cmd > virtualenv env`

Это создаст папку env в текущей директории

Для активации 	
* `env\Scripts\activate.bat`

Для деактивации 
* `env\Scripts\deactivate.bat`

### Далее все действия внутри окружения:

Все зависимости лежат в файле requirements.txt

Для скачивания необходимых зависимостей:
* `pip install -r requirements.txt`
	
Чтобы сделать такой файлик, допустим, при скачивании новых модулей через pip, нужно исполнить следующую команду:
* `pip freeze > requirements.txt`

Если возникнут какие-то ошибки можно попробовать:
* `pip install Django`
* `pip install Pillow`

В будующем этого может стать недостаточно, т.е могут появить еще модули!!!

## Запуск сервера

* Перейти в папку проекта tobacco_project/django/tobaccopoisk
* Выполнить: `manage.py runserver`
* Опционально: после вызова можно указать ip:port
* По дефолту: 127.0.0.1:8000

## Создание юзера в админке

* `manage.py createsuperuser`
* Чтобы войти, к адресу сайта приписываем /admin

## Связь html и питона (шаблоны)

* Соответсвующие html коды помещены в папку
(*<app_name>/templates/<app_name>*) для каждого приложения (tobacco, main и т.д.)

## Работа со статикой
Внутри каждого приложения нужно созавать папку со статикой. Внутри нее файл с именем, совпадающим с названием приложения.

Т.е это будет выглядеть: **/tobaccopoisk/main_page/static/main_page/** 
(*/<project_name>/<app_name>/static/<app_name>/*)

Путь к файлам будет иметь вид: **/tobaccopoisk/main_page/static/main_page/image.jpg** 
(*/<project_name>/<app_name>/static/<app_name>/file*)

### Настройка статики

В settings.py в STATICFILES_DIRS нужно указывать каждое приложение со статикой

Пример для приложения main_page : `os.path.join(BASE_DIR, "main_page/static")`
### Использование в шаблонах
* `{% load static %}`
* `<img src="{% static "main_page/hookah.jpg" %}" alt="My Hookah"/>`

*Больше примеров на сайте Джанго*


## TO DO LIST

- [ ] Добавить механизм обработки тегов
- [ ] Создать механизм для хранения глобальных путей к статике
- [ ] [Перегрузка ImageField](http://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file-with-same-name) для подгрузки в одну папку *(tobacco/static/tobacco/<image_name>)*, а сохранением в БД с другим адресом *(static/tobacco/<image_name>)* :star:
- [ ] Перейти на MySQL :star:
- [ ] Начать заполнять БД табаками
- [ ] Кластеризация данных

## TO TEST LIST

- [ ] Проверить, что при замене фото к табаку через админку, старое фото удаляется
- [ ] Проверить, что поле поиска работает корректно (не алгоритм поиска, а сама кнопка)
- [ ] Проверить, движок поиска. Поиском ошибок 1 рода - очень важно. Поиск ошибок 2 рода - не критичны :rocket:
- [ ] Вынести алгоритм поиска в engine :rocket:
- [ ] Удаление картинки табака при удалении его из БД
- [ ] RESTfull API для поиска
- [ ] Реализовать возможность добавлять в БД имена и бренды с пробелами и заглавными буквами
