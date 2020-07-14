Обеспечение работы нового сайта
================================
## Необходимые пакеты:
* nginx
* Python 3.6
* virtualenv + pip
* Git
например, в Ubuntu:
 sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get install nginx git python36 python3.6-venv
## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domain.com
## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domain.com
## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username
/home/username
└── sites
 └── SITENAME
 ├── database
 ├── source
 ├── static
 └── virtualenv

## служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME на, например, staging.my-domain.com
* заменить SEKRIT почтовым паролем