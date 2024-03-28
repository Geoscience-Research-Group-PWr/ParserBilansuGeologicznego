import logging
from Parser import Parser
logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='parser.log', format='%(asctime)s - %(message)s',level=logging.INFO,filemode="w")
    logger.info("Parser started")
    parser=Parser("Bilans_2012.pdf")
    parser.add_to_db()
    logger.info("Parsing finished")

if __name__=='__main__':
    main()