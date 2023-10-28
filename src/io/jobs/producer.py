from asyncio import Queue, Event
from typing import List, Dict


class Producer:
    """
    Producer:
        - Create jobs
        - Put jobs into queue
    """

    def __init__(self, batch: List[Dict], queue: Queue, on_complete: Event):
        self.batch = batch
        self.queue = queue
        self.on_complete = on_complete

    @classmethod
    async def producer_factory(
        cls, batch: List[Dict], queue: Queue, on_complete: Event
    ):
        """
        This is a factory method that creates a producer for the jobs.
        """
        return cls(
            batch=batch,
            queue=queue,
            on_complete=on_complete,
        )

    async def produce(self) -> None:
        """
        This is the producer method that creates the jobs and puts them into the queue.
        """
        for job in self.batch:
            await self.queue.put(job)

        await self.on_complete.set()
