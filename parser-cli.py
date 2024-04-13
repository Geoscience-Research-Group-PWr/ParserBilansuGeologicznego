import argparse
import csv
import sys
import getpass

import pymongo
from tabulate import tabulate

"""
-h --help 
-v --view #wyświetla dane w terminalu 
-n --name #nazwa kopalni
-r --range #zakres lat, od do 
-e --export #exportuje dane do csv
"""
"""
need to be done:
1. exporting to excel
2. make obligatory arguments (-v or -e)
"""


def part_print(data, batch_size=25):
    for i in range(0, len(data), batch_size):
        print(
            tabulate(
                data[i : i + batch_size],
                headers=["NAZWA", "ROK", "TYP", "WYDOBYCIE", "POWIAT"],
                tablefmt="simple_grid",
                stralign="center",
            )
        )
        if (i + batch_size) < len(data):
            flag = str(
                input(
                    f"Do you want to print another part of data? {len(data)-i-batch_size} left. (y/n): "
                )
            )
            if not (flag == "y" or flag == "yes"):
                sys.exit()
            else:
                print("\n")


def export_to(values):
    # with open(f"", "w")
    ...


def main():
    # parser part
    parser = argparse.ArgumentParser()
    obligatory_group = parser.add_argument_group(
        title="obligatory argument (at least one is required)"
    )
    argument_group = parser.add_argument_group(
        title="possible arguments to narrow results"
    )
    argument_group.add_argument(
        "-n",
        "--name",
        action="store",
        type=str,
        metavar=("NAME"),
        help="narrows the database search by name\n",
    )
    argument_group.add_argument(
        "-r",
        "--range",
        type=str,
        nargs=2,
        metavar=("RANGE FROM", "RANGE TO"),
        help="narrows the database search by range of years from to",
    )
    argument_group.add_argument(
        "-y",
        "--year",
        type=str,
        nargs=1,
        metavar=("YEAR"),
        help="narrows the database search by given year",
    )
    obligatory_group.add_argument(
        "-e", "--export", action="store_true", help="export data to .csv"
    )
    obligatory_group.add_argument(
        "-v", "--view", action="store_true", help="view the data in terminal"
    )
    # mongodb part

    # cli options

    args = parser.parse_args()
    if not (args.export or args.view):
        parser.error(
            "No obligatory arguments provided (-e/-v)\nview --help for more information"
        )

    login = getpass.getpass(prompt="Login to data base: ")
    password = getpass.getpass(prompt="Password to data base: ")
    client = pymongo.MongoClient(
        f"mongodb+srv://{login}:{password}@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client["parser"]
    collection = db["Kopalnie"]

    print(f"ae = {args}")
    query_dict = {}

    if args.name is not None:
        query_dict["Name"] = {"$eq": args.name}

    if args.year is not None:
        query_dict["Year"] = {"$eq": args.year[0]}

    if args.range is not None:
        query_dict["Year"] = {"$gte": args.range[0], "$lte": args.range[1]}

    results = collection.find(query_dict)

    values = [
        [
            *tuple(result.values())[1:4],
            result["More"]["Wydobycie"] if "Wydobycie" in result["More"] else "-",
            result["More"]["Powiat"] if "Powiat" in result["More"] else "-",
        ]
        for result in results
    ]

    if args.export:
        print("export")

    if args.view:
        part_print(values)


if __name__ == "__main__":
    main()
