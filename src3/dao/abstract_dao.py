from abc import ABC, abstractmethod


class AbstractDAO(ABC):
    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, entity_id):
        pass

    @abstractmethod
    def update(self, entity_id, data):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass

