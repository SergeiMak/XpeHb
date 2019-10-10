class Culture:
    Cult_number = 0

    def __init__(self, name):
        self.name = name
        Culture.Cult_number  += 1

        self.number = Culture.Cult_number


def main():
    pakistani = Culture('Pakistani')
    indian = Culture('Indian')




if __name__ == "__main__":
    main()