from abc import ABC, abstractmethod


class AbstractProductDao(ABC):
    @abstractmethod
    def create(self, product):
        pass

    @abstractmethod
    def find_all(self) -> list[dict]:
        pass

    @abstractmethod
    def find_by_id(self, product_id: str) -> dict:
        pass

    @abstractmethod
    def find_by_filter(
        self,
        category: str | None = None,
        min_price: float | None = None,
        search_text: str | None = None,
    ) -> list[dict]:
        pass

    @abstractmethod
    def update(self, product_id: str, fields: dict) -> bool:
        pass

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        pass

