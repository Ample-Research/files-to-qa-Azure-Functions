from datetime import datetime
import logging

def timeit(method):
    def timed(*args, **kw):
        ts = datetime.now()
        result = method(*args, **kw)
        te = datetime.now()
        logging.info(f"{method.__name__} took {te - ts} time to finish")
        return result
    return timed