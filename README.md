**Geological Data Parser**

**Parser Module:**

Parser converts geological data from Polish Geological Institute to CSV files. 
The module enables uploading data to MongoDB databases.

Requirements:

Parser module requirements are listed in requirements.txt.

To install all requirements run this command:

pip install -r requirements.txt

Working with Parser class:

1. Initialize Parser object with Geological Balance Sheet (PDF format).
2. Run **make_directories()** method to ensure all files are created in appropriate directories.
3. Run **parse()** to extract all tables from source PDF.
4. Run **parse_parsed()** to split parsed PDF into PDFs containing only tables related to one mineral type.
5. Run **extract_data()** to convert split PDFs into CSV files.
6. Run **clean_csv()** to create headers and parse through CSV eliminating empty cells.
7. Run **search_csv_for_errors()** to delete unwanted characters from CSV cells
8. Run **add_to_db()** to add clean CSV data to MongoDB collection.

Running these commands will automatically change all files from a given year. To use Parser on a single file run (_one) methods i.ex. extract_one()