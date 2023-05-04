import random
import argparse
import sys
import os

import time
import math
from collections import defaultdict
from datetime import date, timedelta, datetime

import requests
import json

from tweets import TwitterAgent


parser = argparse.ArgumentParser()
parser.add_argument("--prefix", help="runtime prefix path",
                    default="./run")
parser.add_argument("--start", help="start time",
                    default=datetime.now().isoformat())
parser.add_argument("--run-id", help="run-id",
                    default="")
parser.add_argument("--job-id", help="job-id",
                    default="")
parser.add_argument("--data-folder", help="data folder to save",
                    default="./data")
parser.add_argument("--sources", help="sources to pull, comma separated",
                    default="twitter")


def pull_twitter(args):
    agent = TwitterAgent()

    screen_names_famous = os.getenv("TWITTER_LIST_FAMOUS", "")
    screen_names_ai = os.getenv("TWITTER_LIST_AI", "")

    print(f"screen name famous: {screen_names_famous}")
    print(f"screen name ai: {screen_names_ai}")

    agent.subscribe("Famous", screen_names_famous.split(","))
    agent.subscribe("AI", screen_names_ai.split(","))

    data = agent.pull()
    print(f"Pulled from twitter: {data}")

    return data


def save_twitter(args, data):
    """
    Save the middle result (json) to data folder
    """
    filename = "twitter.json"
    data_path = f"{args.data_folder}/{args.run_id}"

    full_path = utils.gen_filename(data_path, filename)

    print(f"Save data to {full_path}")
    utils.save_data_json(full_path, data)


def run(args):
    sources = args.sources.split(",")

    for source in sources:
        print(f"Pulling from source: {source} ...")

        if source == "twitter":
            data = pull_twitter(args)
            save_twitter(args, data)

    
if __name__ == "__main__":
    args = parser.parse_args()

    run(args)
