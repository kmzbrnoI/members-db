# members-db
Members DB

## Run

    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt


## Local checks

    ./pep8-diff.sh
    pylint members-db


## Database setup

    CREATE DATABASE <db_name>;
    CREATE USER '<user>'@'%' IDENTIFIED BY '<password>';
    GRANT ALL PRIVILEGES ON <db_name>.* TO '<user>'@'%';


## Configuration of Google'đ OAuth2
* [dashboard](https://console.cloud.google.com/apis/dashboard)


## Resources
* [docopt](http://docopt.org/)
* [aiohttp](https://docs.aiohttp.org/en/stable/)
* [aiohttp_session](https://aiohttp-session.readthedocs.io/en/stable/reference.html#module-aiohttp_session)
* [aiogoogle](https://aiogoogle.readthedocs.io/en/latest/)
* [asynchronous sqlalchemy](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
