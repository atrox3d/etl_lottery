import logging

from dbhelpers.mysql.db import get_db_url
from etl.extract import get_df_from_html
from etl.load import load_to_mysql
from dbhelpers.mysql.config import build_config

logger = logging.getLogger(__name__)

INPUT_PATH = 'data/in/lotteria.html'
DB_NAME = 'testing'

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO
    )
    logger.info('start etl process')
    
    logger.info(f'loading data')
    winners = get_df_from_html(INPUT_PATH)
    check_nan = winners.isna().values.any()
    assert check_nan == False
    
    logger.info('loading config')
    config = build_config(database=DB_NAME)
    
    logger.info('creating db URL')
    db_url = get_db_url(**config)
    
    logger.info('loading data to mysql db')
    load_to_mysql(winners, db_url)
    
    logger.info('end etl process')
