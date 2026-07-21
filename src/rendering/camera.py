class UICamera:
    def __init__(self,width, height):
        self.width = width
        self.height = height

    def convertPixelToGL(self, x, y):
        newX = (2 * x / self.width) - 1
        newY = 1 - (2 * y / self.height)
        return newX, newY