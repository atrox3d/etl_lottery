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
    ''' get only non null values from dict '''
    return {k:v for k, v in kwargs.items() if v}


def query_builder(sql:str, operator='AND', **kwargs) -> tuple[str, dict]:
    ''' dynamically creates queries vases on kwargs '''

    conditions = []
    params = {}

    kwargs = filter_dict_nulls(**kwargs)
    logger.debug(f'{kwargs = }')

    # PARAM = '%s'    # mysql
    # PARAM = '?'     # sqlite/mysql

    if kwargs:
        for name, value in kwargs.items():
            print(f'{name = }')
            if name.endswith('__like'):
                name = name.replace('__like', '')
                condition = f'{name} like :{name}'
                conditions.append(condition)
                # params.append(format_like(value, middle=True))
                params[name] = format_like(value, middle=True)
            else:
                conditions.append(f'{name} = :{name}')
                # params.append(value)
                params[name] = value
        
        sql = f'{sql} WHERE { f' {operator} ' .join(conditions)}'
        logger.debug(f'{sql = }')
        logger.debug(f'{conditions = }')
        logger.debug(f'{params = }')
        # logger.info(sql % tuple(params)) #FIXME: interpolation
    else:
        logger.debug(f'{sql = }')
    return sql, params