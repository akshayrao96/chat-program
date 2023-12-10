class Message:
    def __init__(self, text):
        self.text = text
        self.next = None


class MessageList:
    def __init__(self):
        self.head = None

    def add(self, text):
        new_message = Message(text)
        if self.head is None:
            self.head = new_message
        else:
            new_message.next = self.head
            self.head = new_message

    def get_next_message(self):
        if self.head is None:
            return None
        message = self.head.text
        self.head = self.head.next
        return message
