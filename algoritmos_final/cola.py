# Cola (FIFO)

from collections import deque

class Cola:
    def __init__(self):
        self.elementos = deque()

    def esta_vacia(self):
        return len(self.elementos) == 0

    def encolar(self, elemento):
        self.elementos.append(elemento)

    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.popleft()
        return None

    def ver_frente(self):
        if not self.esta_vacia():
            return self.elementos[0]
        return None