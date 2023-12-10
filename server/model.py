class Client:

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.next = None


class ClientList:

    def __init__(self):
        self.head = None

    def add(self, name, connection):

        newClient = Client(name, connection)

        # do we have an empty list?
        if self.head is None:
            self.head = newClient

        else:
            newClient.next = self.head
            self.head = newClient

    def nameAvailable(self, name):

        client = self.head

        while client is not None:

            if client.name == name:
                return False

            client = client.next

        return True

    def getByConnection(self, connection):

        client = self.head

        while client is not None:

            if client.connection == connection:
                return client

            client = client.next

        return None

    def drop(self, client):

        temp = self.head
        if temp is None or client is None:
            return

        if temp == client:
            self.head = temp.next
            return

        while temp:

            if temp.next == client:
                temp.next = client.next
                return

            temp = temp.next

    def drop_by_connection(self, connection):
        temp = self.head
        previous = None

        while temp is not None:
            if temp.connection == connection:
                if previous is None:
                    self.head = temp.next
                else:
                    previous.next = temp.next
                return
            previous = temp
            temp = temp.next


class Message:

    def __init__(self, text):
        self.text = text
        self.next = None


class MessageList:

    def __init__(self):
        self.head = None

    def add(self, text):

        newMessage = Message(text)

        # do we have an empty list?
        if self.head is None:
            self.head = newMessage

        else:
            newMessage.next = self.head
            self.head = newMessage
