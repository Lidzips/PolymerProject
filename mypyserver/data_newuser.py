from db_connect import create_connection
from db_connect import execute_query_check_user_exists
from db_connect import execute_query_create_user

def newuser(login, password):
    conn = create_connection("./database/sm_app.sqlite")
    flag = execute_query_check_user_exists(conn, login)
    
    if flag is False:
        execute_query_create_user(conn, login, password)
        return True
    else:
        return False