import pymongo

myclient = pymongo.MongoClient("mongodb://root:rootpassword@localhost:27017")

mydb = myclient["mydatabase"]
collection = mydb.test_collection



dblist = myclient.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")



import datetime
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}


posts = mydb.posts
post_id = posts.insert_one(post).inserted_id
post_id