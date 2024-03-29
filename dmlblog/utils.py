import datetime
import re  # regular expressions
from django.utils.html import strip_tags
import math


def count_words(html_string: str) -> int:
    word_string = strip_tags(html_string)
    words_matched = re.findall(r"\w+", word_string)
    count = len(words_matched)
    return count


def get_read_time(html_string: str) -> str:
    count = count_words(html_string)
    read_time_min = math.ceil(count / 200.0)  # assuming 200wpm reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    read_time = str(datetime.timedelta(minutes=read_time_min))
    return read_time
