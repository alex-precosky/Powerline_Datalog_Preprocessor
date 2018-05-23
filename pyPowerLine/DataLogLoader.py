from abc import ABC, abstractmethod


class DataLogLoader(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def close(self):
        pass
