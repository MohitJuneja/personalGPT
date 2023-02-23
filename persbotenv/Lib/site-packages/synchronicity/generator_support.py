import asyncio
import queue

"""
The plan:
1. Create a new generator
2. Replace the arg in args with the new generator
3. Schedule the coro in the loop


"""

def feed_
class AsyncGenFeeder:
    """Creates an async generator that's thread-safe and can be "fed" from any thread.

    This can be used to keep a sync generator on a main thread but pass an async gen
    to a synchronized method that takes an async generator as an argument.

    TODO: move this to synchronizer later.
    """
    def __init__(self):
        self._queue = queue.Queue()

    def _enqueue(self, done, value):
        future = concurrent.futures.Future()
        self._queue.put((done, value, future))
        ret = future.result()
        return ret

    def feed(self, value):
        return self._enqueue(False, value)

    def close(self):
        return self._enqueue(True, None)

    async def __aiter__(self):
        loop = asyncio.get_event_loop()
        while True:
            done, value, future = await loop.run_in_executor(None, self._queue.get)
            if done:
                future.set_result(None)
                break
            output = yield value
            future.set_result(output)
