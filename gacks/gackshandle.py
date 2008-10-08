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

    def split(self, unit=None, time=None):
        h1 = self.clone()
        h2 = self.clone()

        if unit:
            h1.unitStop = unit
            h2.unitStart = unit

        if time:
            h1.timeStop = time
            h2.timeStart = time

        return (h1, h2)


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
        return self.allocatorHRNs[:]

    def set_consumer(self, consumerHRN):
        self.consumerHRN = consumerHRN

    def get_consumer(self):
        return self.consumerHRN


