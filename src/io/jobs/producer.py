from asyncio import Queue, Event
from typing import List, Dict


class Producer:
    """
    Producer:
        - Create jobs
        - Put jobs into queue
    """

    def __init__(self, batch: List[Dict], queue: Queue, on_complete: Event, **kwargs):
        self.batch = batch
        self.queue = queue
        self.on_complete = on_complete
        self.kwargs = kwargs

    @classmethod
    async def producer_factory(
        cls, batch: List[Dict], queue: Queue, on_complete: Event, **kwargs
    ):
        """
        This is a factory method that creates a producer for the jobs.
        """
        return cls(
            batch=batch,
            queue=queue,
            on_complete=on_complete,
            **kwargs,
        )

    async def produce(self, on_complete: Event):
        """
        This is the producer method that creates the jobs and puts them into the queue.
        """
        for job in self.batch:
            await self.queue.put(job)

        on_complete.set()
