# eCompanyApps
# Graph Database Management
# MSDS 7330 Summer 2018
# Analysts: Daniel Davieau & Luay Dajani
# Summary: Using neo4j graph database to read records (nodes) and relationships and write a record and relationship
# Environment using python 3.7, necessary installed libraries below:
# pip install flask
# pip install neo4j

from neo4j.v1 import GraphDatabase
import pandas as pd
import json
import sys
from flask import Flask, abort, request, jsonify

app = Flask(__name__)

########## METHODS SECTION ##########

#### Helper Methods ####
def db_query(tx, myquery):
    result = ["test"]
    result.pop()
    counter = 0
    for record in tx.run(myquery):
        result.append(record)
    return result

#### Rest Service BASE CASE showing text and python version
@app.route('/')
def index():
	return "This is a sample rest service & json mini-proj MSDS 7330 using python version %s" %sys.version

#### Rest Service definition for returning the data from a specified SQL statement on the ecommerceDB.
@app.route('/simpleQuery', methods=['POST','GET'])
def simpleQuery():

    global query_result
    query_result = ["test"]
    	
    try:
        # Create connection to the neo4j instance running on the local machine
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("msds", "msds"))

        query_result.pop()
        mysession = driver.session()
        query_result = mysession.read_transaction(db_query, "MATCH p=()-[r:Owns]->() RETURN p LIMIT 25")

    except Exception as e:
        print ("Error [%r]" % (e))
        sys.exit(1)
    finally:
        if driver:
            driver.close()
			
	#return jsonify({'SQL Statment': query_result})
    return str(query_result)
    #return "{'GraphDB Query': " + str(query_result) + " }"


########## MAIN SECTION ##########

## Starts the server for serving Rest Services 
if __name__ == '__main__':
    app.run(debug=True)

#print(index())
#result = str(simpleQuery())
#print( "{'GraphDB Query': " + result + " }" )