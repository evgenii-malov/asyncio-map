# encoding: utf-8
__author__ = "Evgeniy Malov"
__version__ = "0.1"
__maintainer__ = "Evgeniy Malov"
__email__ = "evgeniiml@gmail.com"

import asyncio
from itertools import count
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)


class benchmark(object):

    def __init__(self, name, logger):
        self.name = name
        self.logger = logger

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, ty, val, tb):
        end = time.time()
        self.logger.info("%s : %0.3f seconds" % (self.name, end - self.start))
        return False


async def worker(id, queue, coro_func, iterable):
    logger.info("worker started: {}".format(id))
    while True:
        try:
            item = iterable.__next__()
        except StopIteration:
            return
        try:
            r = await coro_func(id, item)
            queue.put_nowait(r)
        except Exception as e:
            logger.exception("error in {}".format(coro_func))


def pool_imap_unordered(loop, workers_count, iterator, coro_func):
    with benchmark("coro map benchmark", logger):
        cnt = count()
        q = asyncio.Queue()

        workers = [asyncio.Task(worker(i, q, coro_func, iterator))
                   for i in range(0, workers_count)]
        while True:
            # check for exit
            if q.empty() and all(w.done() for w in workers):
                break
            # else yield all in queue
            while True:
                try:
                    yield loop.run_until_complete(asyncio.wait_for(q.get(), 3))  #
                except asyncio.QueueEmpty:
                    break
                except asyncio.TimeoutError:
                    break

        logger.info("total items processed: {}".format(cnt.__next__()))
