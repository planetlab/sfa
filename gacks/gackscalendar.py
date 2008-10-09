from gacksexcep import *
from gackshandle import *

class GacksCalendar:
    def __init__(self):
        pass

    def query(self, id=None, unitStart=0, unitStop=INFINITY, timeStart=0, timeStop=INFINITY):
        pass

    def insert_record(self, item):
        pass

    def query_handles(self, handles):
        results = []
        for handle in handles:
            items = query(handle.id, handle.unitStart, handle.unitStop, handle.timeStart, handle.timeStop)
            for item in items:
                if not item.is_in_list(results):
                    results.append(item)
        return results

    def update_record(self, item):
        remove_record(item)
        insert_record(item)

class GacksListCalendar(GacksCalendar):
    def __init__(self):
        self.items = []

    def test_id(self, x, y):
        if not x:
            return True
        else:
            return (x == y)

    def test_lesser(self, x, y):
        if not x:
            return True
        elif y==INFINITY:
            return True
        else:
            return (x<y)

    def test_greater(self, x, y):
        if not x:
            return True
        elif x==INFINITY:
            return True
        elif y==INFINITY:
            return False
        else:
            return (x>y)

    def query(self, id=None, unitStart=0, unitStop=INFINITY, timeStart=0, timeStop=INFINITY):
        list = []
        for item in self.items:
            if self.test_id(id, item.id) and \
               self.test_lesser(unitStart, item.unitStop) and \
               self.test_greater(unitStop, item.unitStart) and \
               self.test_lesser(timeStart, item.timeStop) and \
               self.test_greater(timeStop, item.timeStart):
                 list.append(item)
        return list

    def find_record(self, item_to_delete):
        list = []
        for item in self.items:
            if item.is_same_cell(item_to_delete):
                list.append(item)

        if not list:
            return None

        if len(list) > 1:
            raise GacksMultipleRecordCollision(item_to_delete.as_string())

        return list[0]

    def insert_record(self, item):
        conflicts = self.query(item.id, item.unitStart, item.unitStop, item.timeStart, item.timeStop)
        if conflicts:
            raise GacksConflictingInsert(item.as_string())

        self.items.append(item)

    def remove_record(self, item):
         existing_record = self.find_record(item)
         if existing_record:
             self.items.remove(existing_record)


