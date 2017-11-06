class Queue():
    def __init__(self):
        self.queue = []

    def put(self, element):
        if element not in self.queue:
            self.queue.append(element)

    def get(self):
        while self.queue:
            yield self.queue[0]
            del self.queue[0]

    def __contains__(self, item):
        return item in self.queue
