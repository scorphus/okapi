Okapi
=====

Python Library to send API info to Storage Server

Okapi setup 
===========
In an existing project you should at least modify the following files:

<your-settings-file>
--------------------
Check the existence of the following section under the settings file of your 
project.
```python
[okapi]
name: okapi
replica: <replica-name>
host0: <host0-name>
host1: <host1-name>
host2: <host2-name>
```

requirements/base.txt
---------------------
Add the following requirement line in the proper place (alphabetical order). You 
won't need to add requests if the project is already using it. Anyway requests 
version should be, at least 2.2.11 or greater.
```python
okapi==0.11.0
```

settings/base.py
----------------
Under the database section of the file we should add:
```python
OKAPI_URI = None
if settings.has_section('okapi'):
    OKAPI_URI = 'mongodb://{0},{1},{2}/{3}?replicaSet={4}'.format(
        settings.get('okapi', 'host0'),
        settings.get('okapi', 'host1'),
        settings.get('okapi', 'host2'),
        settings.get('okapi', 'name'),
        settings.get('okapi', 'replica'),
    )
```
We also should add this new section to the file:
```python
########## OKAPI CONFIGURATION
OKAPI_PROJECT = 'your-project-name'
########## END OKAPI CONFIGURATION
```
Note that if the project is already using MongoDB, we shouldn't store Okapi's
data into the same database.

Initialization
--------------
Intialize Okapi in the `models.py` file of a basic application of the project.
This way Okapi will be imported at startup time.

Usage
-----
Once intialized you can use Okapi wherever you use the standard request library.
Think in Okapi as requests because they both have the same API.
[Requests documentation](http://docs.python-requests.org/en/latest/)

Extras
------
### Activating/deactivating okapi in your project.
In the file `settings/base.py` under the OKAPI CONFIGURATION section, you can 
add a boolean setting in order to enable/disable okapi for your project. It 
could be interesting to have it enabled in a pubdev or staging environment and 
when deeply tested, activate it also in production.
You can have a section into your-project-name/settings/dev.py, 

```python
########## OKAPI CONFIGURATION
    OKAPI_ENABLED = True
########## END OKAPI CONFIGURATION
```

Another one into your-project-name/settings/production.py 
```python
########## OKAPI CONFIGURATION
    OKAPI_ENABLED = False
########## END OKAPI CONFIGURATION
```

And so on. Then you could initialize it conditionally as shown below:
```python
http_lib = requests
if (get_custom_setting('OKAPI_ENABLED') and okapi_uri is not None):
    project_name = get_custom_setting('OKAPI_PROJECT', required=True)
    okapi_uri = get_custom_setting('OKAPI_URI', required=True)
    okapi_client = Api(project_name, requests, okapi_uri)
    http_lib = okapi_client
```

