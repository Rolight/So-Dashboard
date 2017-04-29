def key_of_spider_cluster():
    return 'so.core.spiders'


def key_of_spider(spider_name):
    return 'so.core.spiders.{spider_name}'.format(spider_name=spider_name)


def key_of_task_queue():
    return 'so.core.tasks'


def key_of_task_log(task_id):
    return 'so.core.task.{task_id}.log'.format(task_id=task_id)


def key_of_task_command(task_id, command):
    return 'so.core.task.{task_id}.{command}'.format(
        task_id=self.task_id, command=command)
