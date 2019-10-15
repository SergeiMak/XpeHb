class Religion:
    Rel_number = 0

    def __init__(self, name):
        self.name = name
        Religion.Rel_number  += 1

        self.number = Religion.Rel_number


def exist_rel():
    jewish = Religion('Jewish')
    sunni = Religion('Sunni')
    return jewish,sunni
