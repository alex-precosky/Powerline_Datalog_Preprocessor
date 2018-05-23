from abc import ABC, abstractmethod


class DataLogWriter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def close(self):
        pass
