from pymongo import MongoClient

usrname = "kento"
password = "helloworld"
cluster = "cluster0"
database_name = "myjobs"
collection_name = "todo"


def init():
    global client
    global col
    connection_url = "mongodb+srv://"+usrname + \
        ":"+password+"@"+cluster+".foplhch.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_url)
    db = client[database_name]  # database name
    col = db[collection_name]  # collection name


def insert():
    query = [
        {'date': '2021/08/14', 'description': 'ばななを買う'},
        {'date': '2021/08/15', 'description': 'りんごを買う'},
    ]
    x = col.insert_many(query)
    client.close()


def show():
    for item in col.find():
        print(item)


def update():
    query = {'date': '2021/08/14'}
    value = {'$set': {'description': 'おれんじを買う'}}
    col.update_one(query, value)


def delete():
    query = {'date': '2021/08/14'}
    col.delete_one(query)


init()
show()
client.close()
