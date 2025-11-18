class ItemNotFoundError(Exception):
    """Бизнес-ошибка: Item не найден."""

    def __init__(self, item_id: int) -> None:
        super().__init__(f"Item with id={item_id} not found")
        self.item_id = item_id
