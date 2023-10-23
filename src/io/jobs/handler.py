from asyncio import Queue


class Handler:
    """
    Result of jobs:
        - Save to database
        - Save to file

    Task completed callback handler

    Job Completed callback handler
    """

    async def handle_task_results(self, result_queue: Queue):
        """
        This is the method that handles the results of the jobs.
        """
        while True:
            result = await result_queue.get()
            self.task_completed_callback(result)
            result_queue.task_done()

    @staticmethod
    def task_completed_callback(result_queue: Queue):
        """
        This is the result handler method that handles the results of the jobs.
        """
        job = result_queue.get()
        job_id = job["id"]
        print("Handling results for job: " + job_id)

    @staticmethod
    def job_completed_callback(result_queue: Queue):
        """
        This is the job completed handler method that handles the results of the jobs.
        """
        job = result_queue.get()
        job_id = job["id"]
        print("Handling results for job: " + job_id)
