import argparse
import csv
import getpass
import os
import sys

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


def file_name(args):
    if args.name:
        if args.year:
            return f"{args.name}_{args.year[0]}"
        elif args.range:
            return f"{args.name}_{args.range[0]}_{args.range[1]}"
        else:
            return f"{args.name}"
    else:
        if args.year:
            return f"{args.year[0]}"
        elif args.range:
            return f"{args.range[0]}_{args.range[1]}"
        else:
            return "all_records"


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
            if not (flag.lower() == "y" or flag.lower() == "yes"):
                sys.exit()
            else:
                print("\n")


def export_to(values, args):
    working_dir = os.getcwd()
    csv_documents_path = os.path.join(working_dir, "csv_documents")
    if not os.path.exists(csv_documents_path):
        os.mkdir(csv_documents_path)

    os.chdir(csv_documents_path)
    # filename = f"{args.name or ''}_{args.year[0] if args.year else ''}_{args.year[1] if args.year and len(args.year) >1 else ''}"
    filename = file_name(args).replace(" ", "_")

    with open(filename, "w") as file:
        csv_file = csv.writer(file)
        csv_file.writerow(["NAZWA", "ROK", "TYP", "WYDOBYCIE", "POWIAT"])
        csv_file.writerows(values)


def db_connect():
    while True:
        login = getpass.getpass(prompt="Login to data base: ")
        password = getpass.getpass(prompt="Password to data base: ")

        client = pymongo.MongoClient(
            f"mongodb+srv://{login}:{password}@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority"
        )
        try:
            client.admin.command("ping")
            db = client["parser"]
            collection = db["Kopalnie"]
            break

        except pymongo.errors.OperationFailure:
            print("Wrong login/passowrd given")
            response = input("Want try again? (yes/no): ")

            if not (response.lower() == "y" or response.lower() == "yes"):
                sys.exit()

        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    return collection


def parser_args():
    # parser part
    parser = argparse.ArgumentParser()
    obligatory_group = parser.add_argument_group(
        title="obligatory argument (at least one is required)"
    )
    argument_group = parser.add_argument_group(
        title="possible arguments to narrow results"
    )
    exclusive_group = argument_group.add_mutually_exclusive_group()
    argument_group.add_argument(
        "-n",
        "--name",
        action="store",
        type=str,
        metavar=("NAME"),
        help="narrows the database search by name\n",
    )
    exclusive_group.add_argument(
        "-r",
        "--range",
        type=str,
        nargs=2,
        metavar=("RANGE FROM", "RANGE TO"),
        help="narrows the database search by range of years from to",
    )
    exclusive_group.add_argument(
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

    args = parser.parse_args()

    if not (args.export or args.view):
        parser.error(
            "No obligatory arguments provided (-e/-v)\nview --help for more information"
        )
    return args


def main():
    args = parser_args()
    data = db_connect()
    query_dict = {}

    if args.name is not None:
        query_dict["Name"] = {"$eq": args.name}

    if args.year is not None:
        query_dict["Year"] = {"$eq": args.year[0]}

    if args.range is not None:
        query_dict["Year"] = {"$gte": args.range[0], "$lte": args.range[1]}

    results = data.find(query_dict)

    values = [
        [
            *tuple(result.values())[1:4],
            result["More"].get("Wydobycie", "-"),
            result["More"].get("Powiat", "-"),
        ]
        for result in results
    ]

    if args.export:
        export_to(values, args)

    if args.view:
        part_print(values)


if __name__ == "__main__":
    main()
