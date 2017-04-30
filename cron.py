from __future__ import print_function

from pprint import pprint
import os
import yaml
import time
import datetime
import subprocess
import schedule
import sys
import shutil


CRON_UPDATE_TIME = None

def cmd(name, manage=True, log=True):
    if manage:
        cmd_name = "python manage.py %s" % name

    log_name = '_'.join([n for n in name.split() if not n.startswith('-')])
    log_file = open('logs/cron/%s.log' % log_name, 'a')
    f = lambda: subprocess.Popen(
        cmd_name,
        shell=True,
        stdout=log_file if log else open(os.devnull, 'w'),
        stderr=log_file
    )
    f.__name__ = name
    return f

def reload_cron_jobs():
    print('reload jobs')
    schedule.clear()
    with open('cron.yml', 'r') as cron_conf:
        crons = yaml.load(cron_conf)
        for unit,jobs in crons.items():
            if unit == 'day':
                for job in jobs:
                    execute_time, name = job['time'], job['task']
                    log = job.get('log', True)
                    schedule.every().day.at(execute_time).do(cmd(name, log=log))
            else:
                for job in jobs:
                    name = job['task']
                    log = job.get('log', True)
                    time = job.get('time')
                    interval = job.get('interval') or 1
                    sch = getattr(schedule.every(int(interval)), unit)
                    if time:
                        sch = sch.at(time)
                    sch.do(cmd(name, log=log))

def convert():
    def get_line(indent, key, value):
        return indent * '  ' + key + ': ' + value + '\n'
    # backup old yaml file
    shutil.copyfile('cron.yml', 'cron.yml.bak')

    output = ''
    with open('cron.yml', 'r') as cron_conf:
        crons = yaml.load(cron_conf)

    for unit, jobs in crons.items():
        output += unit + ':\n'
        if unit == 'day':
            for job in jobs:
                execute_time, name = job
                output += get_line(1, '- task', name)
                output += get_line(2, 'time', ''.join(["'", execute_time, "'"]))
        else:
            for job in jobs:
                name, interval = job.split('/') if '/' in job else (job, 1)
                output += get_line(1, '- task', name)
                if interval != 1:
                    output += get_line(2, 'interval', interval)

    with open('cron.yml', 'w') as cron_conf:
        cron_conf.write(output)

if __name__ == '__main__':
    if 'convert' in sys.argv:
        convert()
    else:
        while True:
            modify_time = os.path.getmtime('cron.yml')
            print('%s CRON_UPDATE_TIME: %s, modify_time: %s' % (
                datetime.datetime.now(), time.ctime(CRON_UPDATE_TIME),
                time.ctime(modify_time)))
            if CRON_UPDATE_TIME is None or CRON_UPDATE_TIME < modify_time:
                print('=========', time.ctime(CRON_UPDATE_TIME),
                      time.ctime(modify_time))
                reload_cron_jobs()
                CRON_UPDATE_TIME = modify_time
            pprint(schedule.jobs)
            schedule.run_pending()
            time.sleep(60)
