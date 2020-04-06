# Heating/Home Control Systems

This is an experiment in full stack development as I've never done that before.

## Master Control UI

The UI is now functional although backend work is required

To Run you must first install the pipenv, then you can launch the flask app

``` bash
pipenv install
pipenv shell
cd master_control_ui
python wsgi.py
```

The web service listens on <http://localhost.localdomain:8080> so you may have to add a entry to your local hosts file to have 127.0.0.1 listen on that name
