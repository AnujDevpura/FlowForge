from abc import ABC, abstractmethod


class BaseExecutor(ABC):

    @abstractmethod
    async def execute(
        self,
        payload: dict,
    ):
        pass