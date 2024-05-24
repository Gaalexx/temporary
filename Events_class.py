class Event():

    def __init__(self, day, month, year, time, name=None, description=None):
        self.day = day
        self.month = month
        self.year = year
        self.time = time
        self.name = name
        self.description = description
    
    #def __repr__(self) -> str:
    #    return str(self.day) + " " + str(self.month) + " " + str(self.year)