import argparse
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


def part_print(data, batch_size=25):
    for i in range(0, len(data), batch_size):
        print(
            tabulate(
                data[i : i + batch_size - 1],
                headers="firstrow",
                tablefmt="pipe",
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


def export_to():
    ...


def main():
    # parser part
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--name",
        action="store",
        type=str,
        metavar=("name"),
        help="narrows the database search by name\n",
    )
    parser.add_argument(
        "-r",
        "--range",
        type=int,
        nargs=2,
        metavar=("range from", "range to"),
        help="narrows the database search by range of years from to",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=str,
        nargs=1,
        metavar=("year"),
        help="narrows the database search by given year",
    )
    parser.add_argument(
        "-e", "--export", action="store_true", help="export data to .xlsx"
    )
    parser.add_argument(
        "-v", "--view", action="store_true", help="view the data in terminal"
    )
    # mongodb part
    login = str(input("Please give your login to db: "))
    password = str(input("Please give your passwort to db: "))
    client = pymongo.MongoClient(
        f"mongodb+srv://{login}:{password}@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority"
    )  # zmienic password i username na swoje
    db = client["parser"]
    collection = db["Kopalnie"]

    # cli options
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()
        print(f"ae = {args}")
        query_dict = {}

        if args.name is not None:
            query_dict["Name"] = {"$eq": args.name}

        if args.year is not None:
            query_dict["Year"] = {"$eq": args.year[0]}

        if args.range is not None:
            query_dict["Year"] = {
                "$and": [
                    {"Year": {"$gt": str(args.range[0] - 1)}},
                    {
                        "Year": {"$lt": args.range[1]}
                    },  # sprawdzic jak to działa, poki co za malo danych
                ]
            }

        results = collection.find(query_dict) if query_dict else collection.find()

        vals = [
            [
                *tuple(result.values())[1:4],
                result["More"]["Wydobycie"] if "Wydobycie" in result["More"] else "-",
                result["More"]["Powiat"] if "Powiat" in result["More"] else "-",
            ]
            for result in results
        ]
        values = [["Nazwa", "Rok", "Typ", "Wydobycie", "Powiat"]]
        values.extend(vals)

        if args.export:
            print("export")

        if args.view:
            part_print(values)


if __name__ == "__main__":
    main()
