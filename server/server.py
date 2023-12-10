import pygame as pg
import socket


class Client:

    def __init__(self, name):
        self.name = name
        self.next = None


class ClientList:

    def __init__(self):
        self.head = None

    def add(self, name):

        newClient = Client(name)

        if self.head is None:
            self.head = newClient

        else:
            newClient.next = self.head
            self.head = newClient


class Label:

    def __init__(self, text, font):
        self.text = text
        self.font = font

    def draw(self, surface, x, y, color):
        surface.blit(self.font.render(self.text, True, color), (x - 8, y - 15))


class Rectangle:

    def __init__(self, topLeft, size):
        self.rect = (topLeft[0], topLeft[1], size[0], size[1])

    def draw(self, surface, color):
        pg.draw.rect(surface, color, self.rect)


class Button:

    def __init__(self, panel, text, onColor, offColor):
        self.panel = panel
        self.text = text
        self.onColor = onColor
        self.offColor = offColor

    def hasMouse(self):
        (x, y) = pg.mouse.get_pos()
        left = self.panel.rect[0]
        right = self.panel.rect[0] + self.panel.rect[2]
        up = self.panel.rect[1]
        down = self.panel.rect[1] + self.panel.rect[3]

        return x > left and x < right and y > up and y < down

    def draw(self, surface):
        panelColor = self.offColor
        textColor = self.onColor

        if self.hasMouse():
            panelColor = self.onColor
            textColor = self.offColor
        self.panel.draw(surface, panelColor)
        self.text.draw(
            surface, self.panel.rect[0] + 15, self.panel.rect[1] + 15, textColor)


class View:
    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        self.palette = {
            "teal": (41, 127, 135),
            "yellow": (246, 209, 103),
            "light-yellow": (255, 247, 174),
            "red": (223, 46, 46)

        }
        self.font = pg.font.SysFont("calibri", 24)

        self.clientBox = Rectangle((50, 40), (600, 400))

        self.quitButton = Button(
            panel=Rectangle((100, 500), (200, 35)),
            text=Label("Shut Down Server", self.font),
            onColor=self.palette["red"],
            offColor=self.palette["light-yellow"]
        )

        self.clientLabel = Label("...", self.font)
        self.portLabel = Label(f"Listening on port {port}", self.font)

    def shouldExit(self):
        return self.quitButton.hasMouse()

    def drawScreen(self):
        self.screen.fill(self.palette["teal"])
        self.clientBox.draw(self.screen, self.palette["yellow"])
        client = clientList.head
        y = 50

        while client is not None:
            self.clientLabel.text = client.name
            self.clientLabel.draw(self.screen, 100, y +
                                  25, self.palette["red"])
            y += 50
            client = client.next

        self.portLabel.draw(self.screen, 300, 20, self.palette["light-yellow"])
        self.quitButton.draw(self.screen)
        pg.display.update()


class Server:

    def __init__(self):
        pg.init()
        self.host = "localhost"
        self.socket = sock

        self.viewController = View()

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    running = not self.viewController.shouldExit()
            self.viewController.drawScreen()

    def exit(self):
        pass


if __name__ == "__main__":
    server = Server()
    server.run()
    server.exit()
