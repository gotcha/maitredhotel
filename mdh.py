import sys
import os
import argparse
import time
import datetime
from malamute import MalamuteClient


def print_and_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


def trigger(addr, who, url):
    writer = MalamuteClient()
    print_and_flush("connect")
    writer.connect(addr, 100, who)
    print_and_flush("set_producer")
    writer.set_producer(b'mdh')

    while True:
        now = datetime.datetime.now()
        writer.send(url, [b'success', str(now).encode('utf8')])
        time.sleep(10)


def committer(addr, filename, repository):
    git_cmd('git config --global user.email "gotcha@bubblenet.be"')
    git_cmd('git config --global user.name "Godefroid Chapelle"')
    git_cmd('git config --global push.default simple')
    git_cmd('git clone ' + repository)
    os.chdir('mdhtest')
    reader = MalamuteClient()
    print_and_flush("connect")
    reader.connect(addr, 100, b'reader')
    print_and_flush("set_consumer")
    reader.set_consumer(b'mdh', b'')

    while True:
        _, who, url, messages = reader.recv()
        url = url.decode('utf8')
        messages = [msg.decode('utf8') for msg in messages]
        write_and_commit(filename, url, messages)


def write_and_commit(filename, url, messages):
    with open(filename, 'a') as f:
        print(url, *messages, file=f)
    git_cmd('git add ' + filename)
    git_cmd('git commit -m "[Liz-CI] {0}"'.format(url))
    git_cmd('git push')


def git_cmd(cmd):
    print_and_flush(cmd)
    os.system(cmd)

def main():
    parser = argparse.ArgumentParser(description="Maitre d'hotel")
    parser.add_argument(
        '-t', '--trigger',
        action='store_const', const='trigger',
        help='send trigger messages', dest="type"
    )
    parser.add_argument(
        '-c', '--committer',
        action='store_const', const='committer',
        help='commit messages', dest="type"
    )
    parser.add_argument(
        '-a', '--addr',
        action='store', default=b"ipc://@/malamute",
        help="Malamute server address"
    )
    parser.add_argument(
        '-n', '--name',
        action='store', default='trigger', dest='who',
        help="Name of the trigger"
    )
    parser.add_argument(
        '-u', '--url', action='store',
        help="Url of the trigger"
    )
    parser.add_argument(
        '-f', '--filename',
        action='store', default='.mdh',
        help="filename where to commit"
    )
    parser.add_argument(
        '-r', '--repository',
        action='store',
        help="repository where to commit"
    )
    ns = parser.parse_args()
    print_and_flush(ns)
    if ns.type is None:
        print_and_flush("Please specify --trigger or --committer")
    elif ns.type == 'trigger':
        if ns.who is not None and ns.url is not None:
            print_and_flush('trigger')
            addr = ns.addr.encode('utf8')
            url = ns.url.encode('utf8')
            who = ns.who.encode('utf8')
            trigger(addr, who, url)
    elif ns.type == 'committer':
        if ns.repository is not None:
            addr = ns.addr.encode('utf8')
            committer(addr, ns.filename, ns.repository)
    else:
        raise ValueError('Invalid type ' + ns.type)

if __name__ == '__main__':
    print_and_flush('test')
    sys.stdout.flush()
    main()
