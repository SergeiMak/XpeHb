class Culture:
    Cult_number = 0

    def __init__(self, name):
        self.name = name
        Culture.Cult_number  += 1

        self.number = Culture.Cult_number


def exist_cult():
    pakistani = Culture('Pakistani')
    indian = Culture('Indian')
    return pakistani,indian