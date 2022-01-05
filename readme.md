kissom_pg - keep it simple stupid object mapper - postgresql adapter
====================================================================
This project provides the PostgreSQL database adapter for use with kissom

Installation
============
<p>This is meant to be used as a library. To install this project in another project run the following command:

```
    $ pip install git+ssh://git@github.com/joemarchionna/kissom_pg.git
```
My plan is to put this up on PyPI, but until that happens, this how to add it

Dependancies
============
<p>This project uses the following projects:

* kissom
* psycopg2

Use
===
Using the kissom package to access a PostgreSQL database.
Create the manager with the PostgreSQL adapter, obviously substituting your connection details:

```
from kissom.storeManager import StoreManager
from kissom_pg.pgAdapter import PgAdapter

mgr = StoreManager(adapter=PgAdapter(connectionString="host=localhost dbname=databaseName user=databaseUser password=password123"))
```
See the kissom package documentation for a more detailed use description.

Code Formatting
===============
<p>Code formatting was done using BLACK.
<p>To bulk format files, the following command will work:

```
    $ black . -l 119
```

====
