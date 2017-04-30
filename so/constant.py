from so.utils import _const

EVERY_HOUR = 0
EVERY_DAY = 1
EVERY_WEEK = 2
EVERY_MONTH = 3

SCHEDULE_CHOICES = (
    (EVERY_HOUR, '每小时'),
    (EVERY_DAY, '每天'),
    (EVERY_WEEK, '每周'),
    (EVERY_MONTH, '每月'),
)

SCHEDULE_MODE = (
    ('hour', EVERY_HOUR),
    ('day', EVERY_DAY),
    ('week', EVERY_WEEK),
    ('month', EVERY_MONTH),
)

URL_PARSE = 0
URL_WALK = 1
URL_START = 2

URL_CHOICES = (
    (URL_PARSE, '要抓取的页面'),
    (URL_START, '起始页'),
    (URL_WALK, '要经过的页面'),
)

XPATH_PATTERN_TITLE = 0
XPATH_PATTERN_CONTENT = 1
XPATH_PATTERN_CUSTOM = 2

XPATH_PATTERN_CHOICES = (
    (XPATH_PATTERN_TITLE, '标题'),
    (XPATH_PATTERN_CONTENT, '正文'),
    (XPATH_PATTERN_CUSTOM, '自定义'),
)

UNFINISH = 0
FINISH = 1

TASK_STATUS = (
    (UNFINISH, 'unfinished'),
    (FINISH, 'finish'),
)

constant = _const()

for name, value in locals().copy().items():
    if name.isupper():
            setattr(constant, name, value)
