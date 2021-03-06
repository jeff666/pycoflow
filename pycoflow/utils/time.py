from datetime import datetime
from datetime import timedelta


TIME_FORMAT_1 = "%b %d, %Y %H:%M:%S.%f"
TIME_FORMAT_2 = "%Y-%m-%d %H:%M:%S,%f"
TIME_FORMAT_3 = "%b %d, %Y %H:%M:%S,%f"
TIME_FORMAT_4 = "%y/%m/%d %H:%M:%S,%f"
SHORT_TIME_FORMAT_1 = "%H:%M:%S.%f"
SHORT_TIME_FORMAT_2 = "%H:%M:%S,%f"


def convert_epoch_time(epoch_time):
    """
    convert epoch to datetime object
    :param epoch_time: an integer value
    :return: a datetime object
    """
    if isinstance(epoch_time, str):
        epoch_time = float(epoch_time)
    length = len(str(int(epoch_time)))
    if length == 13:
        time_object = datetime.fromtimestamp(epoch_time / 1000)
        micro_seconds = timedelta(milliseconds=(epoch_time % 1000))
        return time_object + micro_seconds
    else:
        time_object = datetime.fromtimestamp(epoch_time)
        return time_object

TIME_CONVERT_FUNCS = [lambda x: datetime.strptime(x, TIME_FORMAT_1),
                      lambda x: datetime.strptime(x, TIME_FORMAT_2),
                      lambda x: datetime.strptime(x, TIME_FORMAT_3),
                      lambda x: datetime.strptime(x, TIME_FORMAT_4),
                      lambda x: datetime.strptime(x, SHORT_TIME_FORMAT_1),
                      lambda x: datetime.strptime(x, SHORT_TIME_FORMAT_2),
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
        elif isinstance(time_express, float):
            return convert_epoch_time(time_express)
        else:
            time_float = time_express.rfind(".")
            if len(time_express) - time_float == 10 and time_express.endswith("000"):
                time_express = time_express[:-3]
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
            return time_object.strftime(TIME_FORMAT_1)

    @staticmethod
    def time_offset(time_object, start_time="Oct 27, 2014 00:00:00.000000000"):
        if not isinstance(start_time, datetime):
            start_time = TimeUtils.time_convert(start_time)
        return (time_object - start_time).total_seconds()

if __name__ == '__main__':
    time_str1 = "Oct 29, 2014 15:28:33.312779000"
    time_str2 = "Oct 29, 2014 00:00:00.000000000"
    t1 = TimeUtils.time_convert(time_str1)
    t2 = TimeUtils.time_convert(time_str2)
    print (t1-t2).total_seconds()
