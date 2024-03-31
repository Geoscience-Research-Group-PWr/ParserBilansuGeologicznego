
# Geological Data Parser

Web and CLI application made for easy parsing of geological balance sheets in PDF format and retrieval of data from MongoDB database.

## Parser Module
Parser converts geological data from Polish Geological Institute to CSV files. The module enables uploading data to MongoDB databases.

Parser module uses various libraries linked in requirements.txt file.

Download all libraries with:
```bash
pip install -r requirements.txt
```
### Working with Parser class
Parser module manipulates multiple files in various formats (PDF,CSV). To ensure correct parsing outputs first copy source PDFs to the same directory as Parser.py and Use.py. Then you can safely run to parse all files at once:
```
python Use.py
```
For working with specific files it is recommended to use _one() methods of the Parser class.

Parser module was made with a goal of parsing Polish Geological Institute balance sheets and therefore it is customized to the templates used by this organization.

## Django Module
This module creates a web application connected with MongoDB database using Django framework. 

If you've run 
```bash
pip install -r requirements.txt
```
already, you have all dependencies installed. Otherwise run:
```
pip install Django~=4.2.11
```
Now run Django web server with:
```
python manage.py runserver
```
For PyCharm users it's possible to run Django server from PyCharm gui. In Run/Debug configurations add a Django server config with enviroment variables:
```
PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=Mines.settings
```
and run it like every other python file.

### Adding content to Django web application
To add some content to the webpage add a function rendering a template in views.py. Then add url path for this template in urls.py. Add a template to templates/MinesAPP directory. Finally in the menu.html add a link to your new template. 
