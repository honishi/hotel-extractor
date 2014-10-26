hotel extractor
==
scrape and extract hotel information from ikyu.com and jalan.net.

setup
--
````
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
````

deploy to heroku
--
````
git push heroku master
````
or, you can push any branch like below.
````
git push heroku develop:master
````

kick in local box
--
````
foreman start
````

test
--
````
py.test tests
````

license
--
copyright &copy; 2014 honishi, hiroyuki onishi.

distributed under the [MIT license][mit].
[mit]: http://www.opensource.org/licenses/mit-license.php
