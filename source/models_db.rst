Database
========

The project uses *MySQL*- object-relational database or ORDBMS with
features such as table inheritance, as well as function overloading.

Our database contains tables:

User
------

.. table:: User

    +--------------------+---------------+-----------------------------+
    | Record name        | Data type     | Description                 |
    +====================+===============+=============================+
    |         id         | Primary key   |  Unique number              |
    +--------------------+---------------+-----------------------------+
    | first_name         | String / text |  User name                  |
    +--------------------+---------------+-----------------------------+
    | last_name          | String / text |  User last name             |
    +--------------------+---------------+-----------------------------+
    | username           | String / text |  User nickname              |
    +--------------------+---------------+-----------------------------+
    | photo_url          | String / text | Url presenter on photo      |
    +--------------------+---------------+-----------------------------+
    | auth_date          | Date time     | User registration time      |
    +--------------------+---------------+-----------------------------+
    | hash               | String / text | Hash code                   |
    +--------------------+---------------+-----------------------------+

BotFunctions
-----------

.. table:: BotFunctions

    +--------------------+---------------+-----------------------------+
    | Record name        | Data type     | Description                 |
    +====================+===============+=============================+
    |         id         | Primary key   |  Unique number              |
    +--------------------+---------------+-----------------------------+
    | func_name          | String / text |  Func name                  |
    +--------------------+---------------+-----------------------------+
    | file_name          | String / text |  Filename                   |
    +--------------------+---------------+-----------------------------+

