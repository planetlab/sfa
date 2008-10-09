##
# This module implements Gacks handles
##

import sys

##
# GacksHandle is an object representing a handle. A handle is the following
# tuple:
#
#    (id, unitstart, unitstop, timestart, timestop)
#
#    id is a text identifier for the resource, for example "CPU"
#
#    unitstart and unitstop form an interval [unitstart, unitstop) in unit
#    space. For example, [0, 10) could represent 10% of a CPU.
#
#    timestart and timestop form an interval [timestart, timestop) in time
#    space.
#
#    If unitstop==INFINITY, or timestop==INFINITY, then it is treated as infinity
#
# The GacksHandle also doubles as an RSPEC

INFINITY = "inf" #sys.maxint

def is_lesser_equal(x, y):
    if x==y:
        return True
    if x==INFINITY:
        return False
    if y==INFINITY:
        return True
    return (x<y)

def is_greater_equal(x, y):
    if x==y:
        return True
    if y==INFINITY:
        return False
    if x==INFINITY:
        return True
    return (x>y)

def interval_contains(start1, stop1, start2, stop2):
    return is_lesser_equal(start1, start2) and is_greater_equal(stop1, stop2)

class GacksHandle:
    def __init__(self, id=None, unitStart=0, unitStop=INFINITY, timeStart=0, timeStop=INFINITY, string=None):
        self.id = id
        self.unitStart = unitStart
        self.unitStop = unitStop
        self.timeStart = timeStart
        self.timeStop = timeStop
        if string:
            self.load_from_string(string)

    def as_string(self):
        return str(self.id) + "#" + \
               str(self.unitStart) + "-" + str(self.unitStop) + "#" + \
               str(self.timeStart) + "-" + str(self.timeStop)

    def parse_range(self, str):
        parts = str.split("-")
        if len(parts)!=2:
            raise ValueError

        if parts[0] != INFINITY:
            parts[0] = int(parts[0])

        if parts[1] != INFINITY:
            parts[1] = int(parts[1])

        return parts

    def load_from_string(self, str):
        parts = str.split("#")

        self.id = parts[0]

        if len(parts) > 1:
            (self.unitStart, self.unitStop) = self.parse_range(parts[1])

        if len(parts) > 2:
            (self.timeStart, self.timeStop) = self.parse_range(parts[2])

    def get_quantity(self):
        if self.unitStop == INFINITY:
            return INFINITY
        else:
            return self.unitStop-self.unitStart

    def get_duration(self):
        if self.timeStop == INFINITY:
            return INFINITY
        else:
            return self.timeStop-self.timeStart

    def dump(self):
        print str(self.id) + ": " + \
              "units " + str(self.unitStart) + "-" + str(self.unitStop) + \
              "time " + str(self.timeStart) + "-" + str(self.timeStop)

    def clone(self):
        return GacksHandle(self.id, self.unitStart, self.unitStop,
                           self.timeStart, self.timeStop)

    def split_subset(self, suStart, suStop, stStart, stStop):
        # an arbitrary rectangle can have a subset removed by slicing it into
        # five pieces:
        #    h1 = top
        #    h2 = left
        #    h3 = right
        #    h4 = bottom
        #    s = subset (middle) that was sliced out

        h1 = self.clone()
        h2 = self.clone()
        h3 = self.clone()
        h4 = self.clone()
        s = self.clone()

        if not suStart:
            suStart = self.unitStart
        if not suStop:
            suStop = self.unitStop
        if not stStart:
            stStart = self.timeStart
        if not stStop:
            stStop = self.timeStop

        h1.unitStop = suStart

        h2.unitStart = suStart
        h2.unitStop = suStop
        h2.timeStop = stStart

        h3.unitStart = suStart
        h3.unitStop = suStop
        h3.timeStart = stStop

        h4.unitStart = suStop

        s.unitStart = suStart
        s.unitStop = suStop
        s.timeStart = stStart
        s.timeStop = stStop

        results = [s, h1, h2, h3, h4]
        valid_results = []
        for result in results:
            if result.get_quantity()>0 and result.get_duration()>0:
                valid_results.append(result)

        return valid_results

    def split_subset_old(self, uStart, uStop, tStart, tStop):
        results = [self]
        if uStart:
            results1 = []
            for i in results:
                results1.extend(i.split_unit(uStart))
            results = results1
        if uStop:
            results1 = []
            for i in results:
                results1.extend(i.split_unit(uStop))
            results = results1
        if tStart:
            results1 = []
            for i in results:
                results1.extend(i.split_time(tStart))
            results = results1
        if tStop:
            results1 = []
            for i in results:
                results1.extend(i.split_time(tStop))
            results = results1
        return results

    def split_unit(self, unit):
        if is_lesser_equal(unit, self.unitStart) or is_greater_equal(unit, self.unitStop):
            return [self]

        h2 = self.clone()

        self.unitStop = unit
        h2.unitStart = unit

        return [self, h2]

    def split_time(self, time):
        if is_lesser_equal(time, self.timeStart) or is_greater_equal(time, self.timeStop):
            return [self]

        h2 = self.clone()

        self.timeStop = time
        h2.timeStart = time

        return [self, h2]

    def is_superset(self, handle):
        if self.id != handle.id:
            return False

        if not interval_contains(self.timeStart, self.timeStop, handle.timeStart, handle.timeStop):
            return False

        if not interval_contains(self.unitStart, self.unitStop, self.timeStart, self.timeStop):
            return False

        return True

    def is_proper_superset(self, handle):
        return self.is_superset(handle) and (not self.is_same_cell(handle))

    def is_same_cell(self, handle):
        return (self.id == handle.id) and \
               (self.unitStart == handle.unitStart) and \
               (self.unitStop == handle.unitStop) and \
               (self.timeStart == handle.timeStart) and \
               (self.timeStop == handle.timeStop)

    def is_same(self, handle):
        return self.is_same_cell(handle)

    def is_in_list(self, handle_list):
        for handle in handle_list:
            if is_same(self, handle):
                return True
        return False

class GacksRecord(GacksHandle):
    def __init__(self, id=None, unitStart=0, unitStop=INFINITY, timeStart=0, timeStop=INFINITY, allocatorHRNs=[], consumerHRN=None):
        GacksHandle.__init__(self, id, unitStart, unitStop, timeStart, timeStop)
        self.allocatorHRNs = allocatorHRNs
        self.consumerHRN = consumerHRN

    def dump(self):
        GacksHandle.dump(self)
        print "  allocators:", ", ".join(self.allocatorHRNs)
        print "  consumer:", self.consumerHRN

    def clone(self):
        return GacksRecord(self.id, self.unitStart, self.unitStop,
                           self.timeStart, self.timeStop,
                           self.allocatorHRNs, self.consumerHRN)

    def set_allocator(self, callerHRN, allocatorHRN, which, where):
        # build up a list of the positions of callerHRN inside of the
        # allocator list

        positions = []
        for i, hrn in enumerate(self.allocatorHRNs):
            if hrn == callerHRN:
                positions.append(i)

        pos = positions[which]

        # truncate the allocator list at the appropriate place.
        # if where==True,
        #     keep callerHRN in the list and append allocatorHRN after
        # otherwise,
        #     remove callerHRN and replace with allocatorHRN

        if where:
            self.allocatorHRNs = self.allocatorHRNs[:(pos+1)]
        else:
            self.allocatorHRNs = self.allocatorHRNs[:pos]

        self.allocatorHRNs.append(allocatorHRN)

    def get_allocators(self):
        return self.allocatorHRNs

    def contains_allocator(self, allocatorHRN):
        return (allocatorHRN in self.allocatorHRNs)

    def set_consumer(self, consumerHRN):
        self.consumerHRN = consumerHRN

    def get_consumer(self):
        return self.consumerHRN

def strings_to_handles(strings):

    # if given a newline-separated list of strings, then expand it into a list
    if isinstance(strings, str):
        expanded_strings = strings.split("\n")
    elif isinstance(strings, list):
        expanded_strings = strings
    else:
        raise TypeError

    # eliminate any blank strings from the list
    non_blank_strings = []
    for string in expanded_strings:
        if string:
            non_blank_strings.append(string)

    handles = []
    for line in non_blank_strings:
        handle = GacksHandle(string = rspec)
        handles.append(handle)

    return handles

def handles_to_strings(handles):
    strings = []
    for handle in handles:
        strings.append(handle.as_string())
    return strings

def rspec_to_handles(rspec):
    return strings_to_handles(rspec)

def find_handle_in_list(list, uStart, uStop, tStart, tStop):
    for item in list:
        if item.unitStart == uStart and \
           item.unitStop == uStop and \
           item.timeStart == tStart and \
           item.timeStop == tStop:
            return item
    return None
