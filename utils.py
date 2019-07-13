import datetime


def timing(f):
    def wrap(*args, **kwargs):
        dt_started = datetime.datetime.utcnow()
        ret = f(*args, **kwargs)
        dt_ended = datetime.datetime.utcnow()
        print('{:s} function took {:f}s'.format(f.__name__, (dt_ended - dt_started).total_seconds()))

        return ret

    return wrap