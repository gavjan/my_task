from RequestHandler import handle, Result
if __name__ == "__main__":
    while True:
        res = handle(input("Enter number of addresses: "), print)
        if res[0] == Result.SUCCESS:
            print("\n-----------Gathered data-----------")
            for country in res[1]:
                print(country)
            exit(0)
        elif res[0] == Result.FATAL:
            print(res[1], file=sys.stderr)
            exit(1)
        else:
            print(res[1])
