""" mdh - Maitre d'hotel

Dependencies for cloud CI

Usage:
    mdh publish [--name=<name>] ADDR URL
    mdh init [--git-email=<email>] [--git-name=<name>] GIT_REPO DEST
    mdh commit [--filename=<filename>] ADDR REPO_DIR

Options:
    -n=<name>, --name=<name>              Publisher name [default: publisher]
    -f=<filename>, --filename=<filename>  Filename where events are committed
                                          [default: .mdh]
"""
import sys
import os
import argparse
import time
import datetime
from malamute import MalamuteClient
from docopt import docopt
import yaml


UTF8 = 'utf8'
PRODUCER = b'mdh'


def print_and_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


def publish(addr, who, url):
    writer = MalamuteClient()
    print_and_flush("connect")
    writer.connect(addr, 100, who)
    print_and_flush("set_producer")
    writer.set_producer(PRODUCER)

    while True:
        now = datetime.datetime.now()
        writer.send(url, [b'success', str(now).encode(UTF8)])
        time.sleep(10)


def init(repository, dest, email, name):
    git_cmd('git config --global user.email "{0}"'.format(email))
    git_cmd('git config --global user.name "{0}"'.format(name))
    git_cmd('git config --global push.default simple')
    git_cmd('git clone {0} {1}'.format(repository, dest))
    os.chdir(dest)


def commit(addr, filename, repository):
    os.chdir(repository)
    reader = MalamuteClient()
    print_and_flush("connect")
    reader.connect(addr, 100, b'reader')
    print_and_flush("set_consumer")
    reader.set_consumer(PRODUCER, b'')

    while True:
        _, who, url, messages = reader.recv()
        url = url.decode(UTF8)
        messages = [msg.decode(UTF8) for msg in messages]
        write_and_commit(filename, url, messages)


def write_and_commit(filename, url, messages):
    with open(filename, 'a') as f:
        print(url, *messages, file=f)
    git_cmd('git add ' + filename)
    git_cmd('git commit -m "[MAITRE D''HOTEL] {0}"'.format(url))
    git_cmd('git push')


def git_cmd(cmd):
    print_and_flush(cmd)
    os.system(cmd)


def main():
    print_and_flush(*sys.argv)
    arguments = docopt(__doc__)
    print_and_flush(arguments)
    if arguments['init']:
        print_and_flush('init')
        init(
            arguments['GIT_REPO'], arguments['DEST'],
            arguments['--git-email'], arguments['--git-name']
        )
    elif arguments['commit']:
        print_and_flush('commit')
        addr = arguments['ADDR'].encode(UTF8)
        commit(addr, arguments['--filename'], arguments['REPO_DIR'])
    elif arguments['publish']:
        print_and_flush('publish')
        addr = arguments['ADDR'].encode(UTF8)
        url = arguments['URL'].encode(UTF8)
        who = arguments['--name'].encode(UTF8)
        publish(addr, who, url)

if __name__ == '__main__':
    main()
