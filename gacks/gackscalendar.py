class GacksCalendar:
    def __init__(self):
        pass

    def query(self, id, unitStart, unitStop, timeStart, timeStop):
        pass

    def insert_record(self, item):
        pass

class GacksListCalendar(GacksCalendar):
    def __init__(self):
        self.items = []

    def test_id(x, y):
        if not x:
            return True
        else:
            return (x == y)

    def test_lesser(x, y):
        if not x:
            return True
        else if y==INFINITY:
            return True
        else:
            return (x<y)

    def test_greater_equal(x, y):
        if not x:
            return True
        else if x==INFINITY:
            return True
        else if y==INFINITY:
            return False
        else:
            return (x>=y)

    def query(self, id, unitStart=0, unitStop=INFINITY, timeStart=0, timeStop=INFINITY):
        list = []
        for item in self.items:
            if test_id(id, item.id) and
               test_lesser(unitStart, item.unitStop) and
               test_greater_equal(unitStop, item.unitStart) and
               test_lesser(timeStart, item.timeStop) and
               test_greater_equal(timeStop, item.timeStart):
                 list = list + item
        return list

    def insert_record(self, item):
        conflicts = self.query(item.id, item.unitStart, item.unitStop, item.timeStart, item.timeStop)
        for conflict in conflicts:
            self.items.remove(conflict)

        self.items.append(item)

