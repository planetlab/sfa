#!/usr/bin/python

class Pretty:
    rows = []
    column_width = []

    def __init__(self, header):
        self.rows.append(header)
        for c in header:
            self.column_width.append(len(header))

    def push_row (self, row):
        self.rows.append(row)
        num = 0
        for c in row:
            if (self.column_width[num] < len(c)):
                self.column_width[num] = len(c)
            num = num + 1
        return

    def pprint (self):
        print '\n'

        for rule in self.rows:
            cur_line = ""
            num = 0

            for r in rule:
                cur_line = cur_line + "%s "%r
                if (self.column_width[num] > len(r)):
                    padding0 = ''.zfill(self.column_width[num] - len(r))
                    padding = padding0.replace('0',' ')
                    cur_line = cur_line + padding
                num = num + 1

            print cur_line


