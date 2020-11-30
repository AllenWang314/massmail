import argparse
import pandas
from os import path

data = None

# parse data.csv
def parse_data():
    if not path.isfile("data.csv"):
        raise Exception("data.csv does not exist")
    df = pandas.read_csv("data.csv")
    print(df)
    print(len(df))


# generates a sample email from data
def generate_sample():
    parse_data()
    return 

# function for getting command line arguments
def getOptions():
    aparser = argparse.ArgumentParser(description="email parameters")
    aparser.add_argument("-sample", action="store_true", help="view sample emails")
    aparser.add_argument("-test", action="store_true", help="test email")
    opts = vars( aparser.parse_args() )
    return opts

def main():
    opts = getOptions()
    if opts["sample"]:
        s = generate_sample()
        print("sample")
    if opts["test"]:
        # generate_test()
        print("test")


if __name__ == "__main__":
    main()