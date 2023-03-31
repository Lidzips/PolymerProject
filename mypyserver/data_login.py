from db_connect import create_connection
from db_connect import execute_query_get_users_role_id

def login(login, password):
    conn = create_connection("./database/sm_app.sqlite")
    flag = execute_query_get_users_role_id(conn, login, password)
    
    if flag == None:
        return 0
    elif flag == 1:
        return 1
    elif flag == 2:
        return 2