import logging

from etl.extract import get_df_from_html
from etl.load import load_to_mysql, get_db_url
from dbhelpers.config import build_config

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    winners = get_df_from_html('data/in/lotteria.html')
    # print(winners)

    config = build_config(database='testing')
    db_url = get_db_url(**config)
    load_to_mysql(winners, db_url)
