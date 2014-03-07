Image Optimizer Service
======================

This is a service which converts image formats and optimizes them. Currently it supports JPEG, PNG and WEBP formats. 

Requirements 
-------------

Image optimizer uses ImageMagick library to perform conversion. The platform must have `libmagickwand` compiled with JPEG, PNG and WEBP support. 

Ther service itself is written in python/Flask

On debian based distros the requirements are installed as follows:

```
apt-get install libmagickwand-dev libjpeg8 libpng libwebp2 python-virtualenv
```

Installation
-------------

After requirements have been met and repository cloned:

1. Create virtualenv for the service and activate it

```
cd ImageOptimizerFrontend
virtualenv .
. bin/activate
```

2. Install python dependencies 

```
pip install -r requirements.txt
```

3. Start production gunicorn server

```
bin/gunicorn -w 4 -b 0.0.0.0:8000 optimizer:app
```

Usage
-------------

To optimize an image make a POST call to optimize method:

```
curl -X POST --data-binary "@image-file.jpg" -H "Content-Type:image/jpeg" http://127.0.0.1:8000/optimize?format=png
```

Supported format parameters are:

* **png** for optimized PNG output
* **jpeg** for optimized JPEG output
* **webp** for optimized WEBP output *if installed ImageMagick library supports it. Check with `identify -list format`*