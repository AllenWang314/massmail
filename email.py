import argparse

# generates a sample email from data
def generate_sample():
    return 

# function for getting command line arguments
def getOptions():
    aparser = argparse.ArgumentParser(description="email parameters")
    aparser.add_argument('-s', '--sample', required=False, type=bool, help='view sample emails')
    aparser.add_argument('-t', '--test', required=False, type=bool, help='test email')
    opts = vars( aparser.parse_args() )
    return opts

def main():
    opts = getOptions()
    if opts["sample"]:
        # s = generate_sample()
        print("sample")
    if opts["test"]:
        # generate_test()
        print("test")


if __name__ == "__main__":
    main()