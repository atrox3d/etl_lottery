import logging


logger = logging.getLogger(__name__)


def format_like(value, start:bool=False, middle:bool=False, end:bool=False) -> str:
    ''' format sql like value to parametrize queries '''

    if middle:
        fmt = f'%{value}%'
    elif start:
        fmt = f'{value}%'
    elif end:
        fmt = f'%{value}'
    else:
        raise ValueError('at least one of start, middle, end is necessary')
    logger.debug(f'{fmt = }')
    return fmt


def filter_dict_nulls(**kwargs) -> dict:
    return {k:v for k, v in kwargs.items() if v}


def query_builder(sql:str, operator='AND', **kwargs) -> str:
    ''' dynamically creates queries vases on kwargs '''

    conditions = []
    params = []

    kwargs = filter_dict_nulls(**kwargs)
    logger.info(f'{kwargs = }')

    # PARAM = '%s'    # mysql
    PARAM = '?'     # sqlite/mysql

    if kwargs:
        for condition, param in kwargs.items():
            if condition.endswith('__like'):
                condition = condition.replace('__like', f' like {PARAM}')
                conditions.append(condition)
                params.append(format_like(param, middle=True))
            else:
                conditions.append(f'{condition} = {PARAM}')
                params.append(param)

        sql = f'{sql} WHERE { f' {operator} ' .join(conditions)}'
        logger.debug(f'{sql = }')
        logger.debug(f'{conditions = }')
        logger.debug(f'{params = }')
        # logger.info(sql % tuple(params)) #FIXME: interpolation
    else:
        logger.info(sql)
    return sql, params