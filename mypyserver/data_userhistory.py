from db_connect import create_connection
from db_connect import execute_query_get_items_by_user_id
import json

def history(login):
    conn = create_connection("./database/sm_app.sqlite")
    queryresult = execute_query_get_items_by_user_id(conn, login)
    
    result = json.dumps(queryresult)
    
    return result