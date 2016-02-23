=======================================
 Python RegExp simple app for reffidle
=======================================

How to install:
---------------------------------------

    #. We need to install python-dev tools.
        sudo apt-get install -y python python-setuptools python-dev python-virtualenv
       
    #. Create virtual environment for this project:
        virtualenv (/path/to/project/)runners/python/.env
        
    #. Then you should install all capabilities for this project in you virtual environment:
        (/path/to/project/)runners/python/.env/bin/pip install -r (/path/to/project/)runners/python/requirements.txt
        
    #. Run application FOR LOCAL USE:
        /path/to/project/)runners/python/.env/bin/python /path/to/project/)runners/python/main.py
         

Settings
---------------------------------------

    By default this application run in :8000 port.
    You may change it if you need in settings.py "PORT" variable.
    
    If You need You can change default routes for this application:
        EVALUATE_URL = '/evaluate'
        REPLACE_URL = '/replace'


RUN IN PRODUCTION SERVER
---------------------------------------
    #. Run application with gunicorn wsgi and nginx:
    
        (/path/to/project/)runners/python/.env/bin/gunicorn main:app
        
        By default this application run in :8000 port.
        You may change it if you need by adding arguments:
            -b ADDRESS, --bind ADDRESS 
                The socket to bind. [['127.0.0.1:8000']]
                
        You can see official documentation about gunicorn:
         http://docs.gunicorn.org/en/latest/run.html
         
         
        Nginx simple configuration:
        
        """
        server {
            listen 80;
         
            root /path/to/hello;
         
            access_log /path/to/hello/logs/access.log;
            error_log /path/to/hello/logs/error.log;
         
            location / {
                proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                if (!-f $request_filename) {
                    proxy_pass http://127.0.0.1:8000;
                    break;
                }
            }
        }
        """
    
    #. Also You can run it with apache wsgi module:
        http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
