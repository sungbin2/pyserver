class Paginator(object):
    def __init__(self, l, n):
        self.items = [l[i:i + n] for i in range(0, len(l), n)]
        self.pageSize = n
        self.pageIndex = 0
        self.max_pageIndex = len(self.items) - 1

    def limit(self):
        if self.pageIndex < 0:
            self.pageIndex = 0
        elif self.pageIndex > self.max_pageIndex:
            self.pageIndex = self.max_pageIndex

    def goto(self, i):
        self.pageIndex = i
        self.limit()
        return self.items[self.pageIndex], self.pageIndex

    def prev(self):
        self.pageIndex -= 1
        self.limit()
        return self.items[self.pageIndex], self.pageIndex

    def next(self):
        self.pageIndex += 1
        self.limit()
        return self.items[self.pageIndex], self.pageIndex

    def over_under(self, b1, b2):
        b1.setEnabled(True)
        b2.setEnabled(True)
        if self.pageIndex <= 0:
            b1.setEnabled(False)
        if self.pageIndex >= self.max_pageIndex:
            b2.setEnabled(False)
