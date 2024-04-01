import logging
import multiprocessing
import os
from Parser import Parser


logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='parser.log', format='%(asctime)s - %(message)s',level=logging.INFO,filemode="w")
    logger.info("Parser started")
    parser=Parser("Bilans_2012.pdf")
    parser.add_to_db()
    logger.info("Parsing finished")
def work(file:str):
    """
    Full parsing with adding to DB.
    :param file: Geological balance sheet
    :return:
    """
    parser=Parser(file)
    logging.basicConfig(filename='parser.log', format='%(asctime)s - %(message)s',level=logging.INFO,filemode="w")
    logger.info("Parser started")
    parser.make_directories()
    parser.parse()
    parser.parse_parsed()
    parser.export_data()
    parser.clean_csv()
    parser.search_csv_for_errors()
    parser.add_to_db()
    logger.info("Parsing finished")


def multitask():
    """
    Creates 4 processes for parsing 4 files in the directory.
    Once one process for a file is finished another file is parsed.
    :return:
    """
    directory = os.getcwd()
    pdfs=[files for files in os.listdir(directory) if files.endswith(".pdf")]
    with multiprocessing.Pool(4) as pool:
            pool.map(work,pdfs)


if __name__=='__main__':
    multitask()