from asyncio import Queue, Event, create_task, gather
from typing import List, Dict, Callable
from src.io.jobs.producer import Producer
from src.io.jobs.consumer import Consumer
from src.io.jobs.handler import Handler


async def _controller(
    batch: List[Dict],
    producer_count: float,
    consumer_count: float,
    processor: Callable,
    handler: Handler,
) -> None:
    """
    This is the controller method that controls the jobs.
    """
    work_queue = Queue()
    result_queue = Queue()

    producer_on_complete = Event()

    # Instantiate the producer
    producer_tasks = [
        create_task(
            Producer.producer_factory(
                batch=batch, queue=work_queue, on_complete=producer_on_complete
            ).produce()
        )
        for _ in range(producer_count)
    ]

    # Instantiate the consumer
    consumer_tasks = [
        create_task(
            Consumer.consumer_factory(
                queue=work_queue,
                processor=processor,
                result_queue=result_queue,
            ).consume(processor=processor, result_queue=result_queue)
        )
        for _ in range(consumer_count)
    ]

    # Instantiate the handler that handles the results of the jobs
    handler_task = create_task(handler.handle_task_results(result_queue=result_queue))

    # Await the completion of producer tasks
    await producer_on_complete.wait()

    # Cancel the consumer tasks when the producer is done
    for consumer in consumer_tasks:
        consumer.cancel()

    # Clean up the consumer tasks
    gather(*consumer_tasks, return_exceptions=True)

    await handler_task

    while not result_queue.empty():
        result = await result_queue.get()
        print("Result: " + str(result))
