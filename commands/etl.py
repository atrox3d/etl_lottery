import logging
import typer

from dbhelpers.mysql.db import get_db_url
from etl.extract import get_df_from_html
from etl.load import load_to_mysql, load_to_sqlite, create_mysql_db
from etl.load import DatabaseError
from dbhelpers.mysql.config import build_config

logger = logging.getLogger(__name__)

INPUT_PATH = 'data/in/lotteria.html'
DB_NAME = 'testing'

app = typer.Typer()


@app.command()
def html2mysql(replace: bool = True, index: bool = True):
    logger.info('start etl process')
    
    logger.info(f'loading data')
    winners = get_df_from_html(INPUT_PATH)
    check_nan = winners.isna().values.any()
    assert check_nan == False
    
    try:
        logger.info('creating config without db name for db creation')
        config = build_config(database=None)
        logger.info('creating db URL without db name')
        db_url = get_db_url(**config)
        
        logger.info('creating db')
        create_mysql_db(db_url, DB_NAME)
    except Exception as e:
        logger.error('could not create database')
        exit(1)
    
    try:
        logger.info('creating default config with db name')
        config = build_config(database=DB_NAME)
        
        logger.info('creating db URL')
        db_url = get_db_url(**config)
    
        logger.info('loading data to mysql db')
        load_to_mysql(winners, db_url)
        logger.info('end etl process')
    except DatabaseError as e:
        logger.error(e)
        logger.fatal('problems with mysql db, exiting')
        exit(1)


@app.command()
def html2sqlite(
        dbname  : str  = DB_NAME,
        replace : bool = True, 
        index   : bool = True
    ):
    logger.info('start etl process')
    
    logger.info(f'loading data')
    winners = get_df_from_html(INPUT_PATH)
    check_nan = winners.isna().values.any()
    assert check_nan == False
    
    # logger.info('creating default config')
    # config = build_config(database=DB_NAME)
    # 
    # logger.info('creating db URL')
    db_url = f'sqlite:///{dbname}.db'
    
    logger.info('loading data to sqlite db')
    load_to_sqlite(winners, db_url)
    
    logger.info('end etl process')
