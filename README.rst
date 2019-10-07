Readme
======

acdh-django-transkribus
------------

a django-app for transkribus


A django app for interacting with the [Transkribus-API](https://transkribus.eu/wiki/index.php/REST_Interface) to search and read documents hosted and processed by [Transkribus](https://transkribus.eu/Transkribus/)

Installation
------------

    pip install acdh-django-transkribus

Use:
------------

TRANSKRIBUS-Settings

Basically your user name and password and the ID of the collection you'd like to expose by the current application.


    TRANSKRIBUS = {
        "user": "mytranskribususer@whatever.com",
        "pw": "mytranskribuspassword",
        "col_id": "43497",
        "base_url": "https://transkribus.eu/TrpServer/rest"
    }



Licensing
---------

All code unless otherwise noted is licensed under the terms of the MIT License (MIT). Please refer to the file LICENSE in the root directory of this repository.
