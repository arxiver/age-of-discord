
![introducy-gif](https://media.giphy.com/media/zgduo4kWRRDVK/giphy.gif)

#### TLDR
That's an article about Graph databases gives you a very quick introduction about it and specifically Apache AGE and for the sake of understanding a very simple discord application will be implemented, I hope you enjoy reading it and gives you some new insights and information.  

### Pilot of the AGE

When I was a **student** I've **heard** a lot of **thoughts** from **teachers** while having the **database** or **algorithms** lectures and sections that if you are going to create a **social network** application **database** the best **representation** for it the **graph** data **structure** but for the **SQL's being** we need to **normalize** that **graphs** to fit into our **tables** 

In the following article I am going to guide you to the truth and tell you everything they have not let us know!

 ![are-you-ready](https://media.giphy.com/media/XHX9s5YLavonUU4Cbr/giphy.gif)

<hr/> 

### Comparison 

<center> From: <b>Designing Data Intensive Applications</b>
</center>

- Query using relational database structured query language
![Graph-on-relational-query](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xnsy7xyogbhwq9sto9ha.png)

- Query using cypher and graph database
![Graph-on-cypher](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r3adj4ai0lfybwymio5e.png)

<hr/> 

### What is going on?
- Introduction to **graph databases**
- Learn about AGE & learning a little about **OpenCypher**
- Creating simple app demonstrating the idea (**Simple Discord**)

<hr/> 

### Inspiration

- Our communication channel on Apache age is **Discord**
- Some talks about the **graph** databases performance 

<hr/> 

#### Prerequisites 

 - PostgreSQL installed
 - Apache AGE installed with correct version of PostgreSQL
 - Cypher Syntax very little knowledge is okay also I will cover some review 

<hr/> 

### Brief introduction to what is the relation between AGE and PostgreSQL

![killua](https://media.giphy.com/media/qb1eHxhUHLdsc/giphy-downsized-large.gif)


<center>
That's how PostgreSQL looks like when we execute that
</center>

```SQL
LOAD 'age';
```

<hr/> 

Let's **dive** into in a **very short terms** what are **Apache AGE** and **PostgreSQL** and their **connections** 


#### Apache AGE

It is a PostgreSQL extension that provides graph database functionality. That means we could have the relational database alongside the graph database

####  PostgreSQL

PostgreSQL is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance. 

####  PostgreSQL and Apache AGE

As mentioned before having the extension AGE on top of PostgreSQL allowing you to enable a new feature of the graph databases on top of the structured relational databases, i.e. adding the OpenCypher query language to the SQL language into a single language.

### Cypher querying review:

<center> <h4> Create new graph </h4> </center>

```SQL
 SELECT * FROM create_graph('dev-graph');
```
![Create new graph](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ita6uvcnx8wwog8wueyd.png)

<hr/> 


<center> <h4> Create nodes and edge </h4> </center>

![querying review](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zufhebra6y6zyz09dksi.png)
That query creates a **node** (AS n) of type/label **DEVELOPER** with **properties** _name_, _role_ and _department_ and connects it throw **edge** (AS e) with type/label **MANAGES** to another **node** (AS d) of type/label **DEPARTMENT** with **properties** _name_  and returns them

**Explanation:**
-    (): Everything is wrapped with () is a node
-    []: Everything is wrapped with () is an edge
-    [str:] : str is an alias to hold the edge or if within () the node to mention it in the rest of the query
-    (str: LABEL): LABEL is the category or the label of the node
-    {}: called properties of json type that holds any info you want to add

<hr/> 

<center> <h4> Query the graph </h4> </center>

![Query the graph](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/in2oe11poo6jc7p4wnnc.png)



```SQL
test=#  SELECT * FROM cypher('dev-graph', $$
MATCH (n:DEVELOPER)-[m:MANAGES]->(d:DEPARTMENT) return n, d
$$) as (n agtype, d agtype);
                                                                    n | d                           

+----------------
 {"id": 844424930131969, "label": "DEVELOPER", "properties": {"name": "Mark", "role": "Head of Engineering", "department": "IT"}}::vertex | {"id": 1407374883553281, "label": "DEPARTMENT", "properties": {"name":
 "IT"}}::vertex
(1 row)
```

<hr/>

### Question comes to mind

- Why for every cypher call should I make 
```SQL
SELECT * from cypher( -- bla bla bla
```
<center>
<b> Why cannot I write cypher directly? </b>
</center>

The answer in very short terms and words because **AGE** is an extension on top of PostgreSQL it is being injected to the **PostgreSQL** **backend** as a **function call** like the **PL/SQL** functions you are doing and while the working inside it **turns into a query tree** and **gets** **involved** on the query through **replacing** the **function call** _with_ a **sub query/ies** based on what was inside the cypher so at the end we get a **Query Tree** is being executed by the executor of the **PostgreSQL** at the end.

```SQL
SELECT * FROM (NEW QUERY INJECTED HERE)
```
</hr>

**That point** introduces us to a very nice project that our team has building for the sake of **user experience** **enhancements** called **AgeSQL** that wraps the cypher call with the repeated portion so that you can start with the cypher query directly, you will find the link on the references 

**And** for sure we cannot forget mentioning the project of **AGE Viewer** which is one of the interesting projects that is used for the graph visualizations 

The being of having a single container for our data both the structured data and non structured data (Graph database **alongside** SQL) is one of the key features that supports the **usage** of **AGE** and **specifically** being part of **PostgreSQL** is a high valuable point. 

<hr/>

<center>
<h2> Let's Build the APP </h2>
</center>

![letsgoo](https://media.giphy.com/media/l0HlxJMw7rkPTN8sg/giphy.gif)

### Setup Environment

I am going to use Python3.10 and PostgreSQL 13 alongside Apache AGE 1.3.0 (PG13 version)

PostgreSQL installation:

```sh
wget https://ftp.postgresql.org/pub/source/v13.3/postgresql-13.3.tar.gz

tar xzf postgresql-13.3.tar.gz
cd postgresql-13.3/

mkdir data
chown $(whoami) data

./configure --prefix=$(pwd) --enable-debug
make
make install

export LD_LIBRARY_PATH=$(pwd)/lib
export PATH=$PATH:$(pwd)/bin

echo export PG_PATH=$(pwd) >> ~/.bashrc
echo export LD_LIBRARY_PATH=$(pwd)/lib >> ~/.bashrc
echo export PATH=$PATH:$(pwd)/bin >> ~/.bashrc

# initialize the data directory
./bin/initdb -D ./data

# start the server
./bin/postgres -D ./data >logfile 2>&1 &

# create db named test
./bin/createdb test

./bin/psql test

```

AGE installation

```sh
wget https://github.com/apache/age/releases/tag/PG13/v1.3.0-
rc0
tar xzf apache-age-1.3.0-src.tar.gz
cd apache-age-1.3.0

echo export AG_PATH=$(pwd) >> ~/.bashrc

make PG_CONFIG=$(PG_PATH)/pg_config install
make PG_CONFIG=$(PG_PATH)/pg_config installcheck

psql test
CREATE EXSTENSION age;
LOAD 'age';
SELECT * FROM ag_catalog.create_graph('test');
```
Congrats you are having a working environment now :)
![deadpool again](https://media.giphy.com/media/LXiElF2dzvUmQ/giphy.gif)

<hr/>


### Python Environment 

```sh
mkdir discord
git init
virtualenv venv
source venv/bin/activate
touch requirements.txt
```

Add the following (that's the same of the driver of age)

```
psycopg2 --no-binary :all: psycopg2
antlr4-python3-runtime==4.11.1
setuptools
```
Save and **run pip3 install -r requirements.txt**

Then install age driver

```sh
cd $(AG_PATH)/drivers/python
python setup.py install
# Go back to AG_PATH
cd $(AG_PATH)
```

You are now supposed having a running python **AGE** environment 


![deadpool2](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGg4bnIzdWFsMGRtdGY3c2RycHpraGE4MWdsOWVxbmhwNXVlM3g3NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NSDmc1yecieZBbMSFG/giphy.gif)

#### Graph creation

- Create new graph
```sql 
LOAD 'age';
SET search_path = ag_catalog;
SELECT * FROM create_graph('discord');
```
As it is a simple discord we are going to treat the server as single channel 

#### Schematic
- User
 - ID
 - Username
 - Full name
- Server
 - ID
 - Name
- Message
 - ID
 - Content

#### Relations
- (User) -[Member]-> (Server) 
- (User) -[Message]-> (User|Server)

#### Endpoints

- CREATE
 - Create User
 - Create Server
 - Join Server
 - Send Message

- MATCH
 - Get User
 - Get Server
 - Get Messages


Let's get started

```sh
touch main.py
```

Create connection

`db.py`

``` python
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


```

- Setup query wrapper to avoid writing select * from every time, also at `db.py`

```python
def execute_query(conn, graph_name, query, return_count=1):
    if graph_name == None:
        raise ValueError("Graph name is not provided")
    if query == None:
        raise ValueError("Query is not provided")
    as_statement = ", ".join([f"v{i} agtype" for i in range(return_count)])
    print(f"SELECT * FROM cypher('{graph_name}', $$ {query} $$) as ({as_statement});")
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                f"SELECT * FROM cypher('{graph_name}', $$ {query} $$) as ({as_statement});",
            )
            for row in cursor:
                print("CREATED::", row)
            conn.commit()
            return cursor
        except Exception as ex:
            conn.rollback()
            print(type(ex), ex)

# The function that will be used on the querying as a top level 
def eq(query, rc=1):
    """
    Execute query (eq) wrapper it takes the query as an openCypher langauge
    and executes it also it requires having the count of the returns (rc: return count)

    Args:
        - query: string OpenCypher query starts which (MATCH, CREATE, etc)
        - rc: int number of the returned nodes+edges on the query default 1 return
    """
    return execute_query(conn, graph_name, query, rc)
```

- Create user function 
```python
def create_user(name, username) -> age.Vertex:
    # Validate that user with the same username does not exist
    exisiting_user = find_user(username)
    if exisiting_user:
        raise ValueError("Duplicate username")
    
    cur = eq(
        f"""CREATE (u:User {{username: "{username}", name:"{name}"}}) RETURN u """,
        1,
    )
    res = cur.fetchall()
    if (len(res) > 0):
        res = res[0][0]
    cur.close()
    return res
```

- Find user

```python

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
```

- Create server

```python

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

```

- Join server

```python
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
```

- Send message to

```python

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

```

- Get messages of 
```python

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
```

- Main

```python
from db import create_user, create_server, join_server, send_message_to, get_messages_of

if __name__ == '__main__':
  # Create user 
  user1 = create_user("Mohamed", "mohamed")
  
  # Create another user 
  user2 = create_user("Ahmed", "ahmed")

  # Create server
  server = create_server("AgeDB")

  # Join server
  join_server(user1.properties["id"], server.properties["id"])

  # Send message to user
  send_message_to(user1.properties["id"], user2.properties["id"], "User", "Hello Ahmed!")
  send_message_to(user1.properties["id"], user2.properties["id"], "User", "Hello Ahmed 2!")

  # Send message to server
  send_message_to(user1.properties["id"], server.properties["id"], "Server", "Hello Server!")

  # Get messages of user
  user1_messages = get_messages_of(user1.properties["id"])
  
  # Print messages of user
  for message in user1_messages:
      print(message.toJson())
```
<hr/>


All codes are provided in the following [repository](https://github.com/rrrokhtar/age-of-discord)

<hr/>
### Conclusion

In that article I have tried to give you a brief **introductory** to the **graph databases** and the ability to use it on applications as well as specifically giving an example of usage of **Apache AGE** alongside **PostgreSQL** which allows you to have **relational** database **supported** by the extension of **Graph** databases which makes you enjoy all of the key **features of PostgreSQL** and its **robustness** in **addition** to getting **AgeDB** beside that as well as a simple lesson about OpenCypher it has been provided also. I hope you find the article as a useful resource and gives you the **initial** steps of your **journey** with the **graph databases** 

<hr/>

<center>
<h3>End of the article</h3>
</center>

![thanks-levi](https://media.giphy.com/media/9KCPkAcRqU9j2/giphy.gif)

<center>
Thank you for reaching here and reading my blog :)
</center>

### References and resources:

- [Does your app needs AGE](https://dev.to/rrrokhtar/does-your-app-need-apache-age-i23)
- [AGE Offical](https://age.apache.org/)
- [Postgres-and-Apache-AGE](https://sorrell.github.io/2020/12/10/Postgres-and-Apache-AGE.html)
- [AGE journey](https://bitnine.net/blog-postgresql/apache-age-journey-top-level/)
- [AGE on GitHub](https://github.com/apache/age)
- [Postgres-with-Apache-AGE](https://dev.to/rrrokhtar/dev-age-16-with-postgres-16-4pfk)
- [10 Reasons why to use AGE](https://dev.to/rrrokhtar/10-reasons-why-to-use-apache-age-alongside-postgresql-iib)
- [How AGE is executed on top of PostgreSQL](https://dev.to/rrrokhtar/how-age-is-executed-on-top-of-postgresql-4mpf)
- [Behind the scenes of AGE](https://dev.to/rrrokhtar/whats-behind-scenes-of-apache-age-23f2)
- [Graph Database and NoSQL](https://dev.to/rrrokhtar/graph-database-and-nosql-52ek)
- [AGE official installation](https://age.apache.org/age-manual/master/intro/setup.html#installation)
