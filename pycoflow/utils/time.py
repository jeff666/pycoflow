from datetime import datetime
from datetime import timedelta

TIME_FORMAT_ONE = "%b %d, %Y %H:%M:%S.%f"
TIME_FORMAT_TWO = "%Y-%m-%d %H:%M:%S,%f"
SHORT_TIME_FORMAT = "%H:%M:%S.%f"


def convert_epoch_time(epoch_time):
    """
    convert epoch to datetime object
    :param epoch_time: an integer value
    :return: a datetime object
    """
    length = len(epoch_time)
    if isinstance(epoch_time, str):
        epoch_time = int(epoch_time)
    if length == 13:
        time_object = datetime.fromtimestamp(epoch_time / 1000)
        micro_seconds = timedelta(milliseconds=(epoch_time % 1000))
        return time_object + micro_seconds
    elif length == 10:
        time_object = datetime.fromtimestamp(epoch_time)
        return time_object

TIME_CONVERT_FUNCS = [lambda x: datetime.strptime(x, TIME_FORMAT_ONE),
                      lambda x: datetime.strptime(x, TIME_FORMAT_TWO),
                      lambda x:convert_epoch_time(x)]


class TimeUtils(object):
    @staticmethod
    def time_convert(time_express):
        """
        convert time string to datetime object
        :param time_express: a description of time
        :return: a datetime obiect
        """
        if isinstance(time_express, datetime):
            return time_express
        else:
            for func in TIME_CONVERT_FUNCS:
                try:
                    converted_time = func(time_express)
                except ValueError:
                    pass
                else:
                    return converted_time
            raise ValueError('Error: format error of: %s' % time_express)

    @staticmethod
    def time_delta_convert(duration):
        """
        convert duration to timedelta object
        :param duration: in seconds (float)
        :return: a timedelta object
        """
        if isinstance(duration, timedelta):
            return duration
        else:
            return timedelta(seconds=duration)

    @staticmethod
    def time_to_string(time_object, time_format=''):
        """
        datetime object to string value
        :param time_object: a datetime object
        :param time_format: expected time format
        :return: a string
        """
        assert isinstance(time_object, datetime), "Error: %s should be an instance of datetime"
        if time_format:
            return time_object.strftime(time_format)
        else:
            return time_object.strftime(TIME_FORMAT_ONE)