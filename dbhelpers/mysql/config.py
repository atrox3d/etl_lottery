import logging
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SECRETS_PATH = '.secrets'
logger = logging.getLogger(__name__)


def get_password_from_secrets(
        password_filename:str='password.txt',
        secrets_path:str=SECRETS_PATH
) -> str:
    password_path = Path(secrets_path, password_filename)
    return password_path.read_text().strip()


def build_config(
        host:str='localhost',
        user:str='root',
        password:str=get_password_from_secrets(),
        database:str|None=None
) -> dict:
    return dict(
        host=host,
        user=user,
        password=password,
        database=database
    )


def save_config(
        config:dict,
        config_filename:str='config.json',
        secrets_path:str=SECRETS_PATH
):
    config_path = Path(secrets_path, config_filename)
    with open(config_path, 'w') as fp:
        json.dump(config, fp, indent=4)


def load_config(
        config_filename:str='config.json',
        secrets_path:str=SECRETS_PATH
) -> dict:
    config_path = Path(secrets_path, config_filename)
    with open(config_path, 'r') as fp:
        return json.load(fp)


def get_default_config(
        config_filename:str='config.json',
        secrets_path:str=SECRETS_PATH
) -> dict:
    try:
        logger.info(f'loading {secrets_path}/{config_filename}')
        return load_config(config_filename, secrets_path)
    except:
        logger.warning(f'loading failed, returning default')
        return build_config()
