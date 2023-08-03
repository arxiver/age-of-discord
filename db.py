import uuid
import psycopg2
import age
import os

graph_name = os.environ.get("GRAPH_NAME", "test")
host = os.environ.get("GRAPH_NAME", "localhost")
port = os.environ.get("PORT", "5432")
dbname = os.environ.get("DB_NAME", "test")
user = os.environ.get("USERNAME", "rrr")
password = os.environ.get("PASSWORD", "")

conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)

if conn == None:
    raise ConnectionError("Connection to database failed")

age.setUpAge(conn, graph_name)


def execute_query(conn, graph_name, query, return_count=1):
    if graph_name == None:
        raise ValueError("Graph name is not provided")
    if query == None:
        raise ValueError("Query is not provided")
    as_statement = ", ".join([f"v{i} agtype" for i in range(return_count)])
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM cypher('{graph_name}', $$ {query} $$) as ({as_statement});",
        )
        conn.commit()
        return cursor
    except Exception as ex:
        conn.rollback()
        print(type(ex), ex)


def eq(query, rc=1):
    """
    Execute query (eq) wrapper it takes the query as an openCypher langauge
    and executes it also it requires having the count of the returns (rc: return count)

    Args:
        - query: string OpenCypher query starts which (MATCH, CREATE, etc)
        - rc: int number of the returned nodes+edges on the query default 1 return
    """
    return execute_query(conn, graph_name, query, rc)


def find_user(username) -> age.Vertex:
    cur = eq(
        f"""MATCH (u:User {{username: "{username}"}}) RETURN u """,
        1,
    )
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0][0]
    cur.close()
    return res

def find_user_by_id(id) -> age.Vertex:
    cur = eq(
        f"""MATCH (u:User {{id: "{id}"}}) RETURN u """,
        1,
    )
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0][0]
    else:
        res = None
    cur.close()
    return res

def create_user(name, username) -> age.Vertex:
    # Validate that user with the same username does not exist
    # exisiting_user = find_user(username)
    # if exisiting_user:
    #     raise ValueError("Duplicate username")
    id = uuid.uuid4()
    cur = eq(
        f"""CREATE (u:User {{username: "{username}", name:"{name}", id: "{id}"}}) RETURN u """,
        1,
    )
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0][0]
    cur.close()
    return res


def create_server(name) -> age.Vertex:
    id = uuid.uuid4()
    cur = eq(
        f"""CREATE (s:Server {{name: "{name}", id:"{id}"}}) RETURN s """,
        1,
    )
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0][0]
    cur.close()
    return res


def find_server_by(property, value):
    cur = eq(
        f"""MATCH (s:Server {{{property}: "{value}"}}) RETURN s """,
        1,
    )
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0][0]
    cur.close()
    return res


def join_server(user_id, sever_id):
    cur = eq(
        f"""MATCH (u:User {{id: "{user_id}"}}), (s:Server {{id: "{sever_id}"}}) 
        CREATE (u)-[e:Member]->(s)
        RETURN e """,
        1,
    )
    if cur == None:
        raise Exception("Incorrect ids provided")
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0][0]
    cur.close()
    return res


def send_message_to(from_id, to_id, to_type, message_content):
    if to_type != "User" and to_type != "Server":
        raise ValueError("Incorrect message direction")
    
    from_user = find_user_by_id(from_id)
    if from_user == None:
        raise Exception("Non-exisiting from user")
    
    # Check authorization
    if to_type == "Server":
        cur = eq(
            f"""MATCH (u:User {{id: "{from_id}"}}) -[]- (x:Server {{id: "{to_id}"}}) RETURN u """,
            1,
        )
        res = cur.fetchall()
        if res == None:
            cur.close()
            raise Exception("Unauthorized")
        cur.close()
    else:
        to_user = find_user_by_id(to_id)
        if to_user == None:
            raise Exception("Non-exisiting from user")
        
    cur = eq(
        f"""MATCH (u:User {{id: "{from_id}"}}), (x:{to_type} {{id: "{to_id}"}})
          CREATE (u)-[m:Message {{content:"{message_content}", from:"{from_id}", to:"{to_id}"}}]->(x)
          RETURN m
          """,
        1,
    )
    if cur == None:
        raise Exception("Failed to create the message")
    res = cur.fetchall()
    if len(res) > 0:
        res = res[0][0]
    cur.close()
    return res


def get_messages_of(user_id) -> list[age.Edge]:
    cur = eq(
        f"""MATCH (u:User {{id: "{user_id}"}})-[m:Message]->(x)
        RETURN m """,
        1,
    )
    if cur == None:
        return []
    res = cur.fetchall()
    res = [r[0] for r in res]
    cur.close()
    return res