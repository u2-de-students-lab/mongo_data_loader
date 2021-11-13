import argparse
import json
import os
from argparse import Namespace

from dotenv import load_dotenv
from pymongo import MongoClient


def cli() -> Namespace:
    parser = argparse.ArgumentParser(description="This script parse the path you've paste and load the data "
                                                + "into MongoDB database.\nYour file should be JSON!")
    parser.add_argument('user_json', type=str, help='Put path to ur json file')
    cli_arguments  = parser.parse_args()

    return cli_arguments 


def load_to_mongo(path: str) -> None:
    client = MongoClient(os.environ.get('DB_PATH'))
    db = client[os.environ.get('DB_NAME')]
    db_collection = db[os.environ.get('DB_COLLECTION')]
        
    with open(path) as fl:
        data = json.load(fl)

    if isinstance(data, list):
        db_collection.insert_many(data)  
    else:
        db_collection.insert_one(data)


def main() -> None:
    arguments = cli()
    load_dotenv()
    load_to_mongo(path=arguments.user_json)


if __name__ == '__main__':
    main()