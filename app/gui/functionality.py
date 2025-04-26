import random
import config
from typing import Union, List
from app.constants import QueryString as Query, AppDataConstants as AppConst
from utils import db_util as db


def choose_random_project(current_project_id):
    database: str = config.DATABASE_URL
    query: str = Query.PROJECT_ALL_IDS
    return_list: Union[str, list]
    data_extract: List = db.dql_fetch_all_rows(database=database, sql_script=query, return_list=True)
    data_extract.remove(current_project_id)
    if AppConst.RANDOM_PROJECT_GEN_COUNT == 1:
        return_list = random.choice(data_extract)
    else:
        return_list = []
        for count in range(AppConst.RANDOM_PROJECT_GEN_COUNT):
            return_list.append(random.choice(data_extract))
    return return_list


