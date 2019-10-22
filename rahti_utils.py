import errno
import fcntl
import os
import tempfile
import time
import urllib.request


def download_file(url):
    filename = os.path.join(tempfile.gettempdir(), os.path.basename(url))

    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    # Use file locking to prevent many processes from downloading the
    # same file at the same time ...
    fp = open(filename, 'a')
    was_locked = False
    while True:
        try:
            fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError as e:
            if e.errno != errno.EAGAIN:
                raise
            else:
                # if it was locked, we will just wait for it to become
                # unlocked, i.e., when the download is complete
                if not was_locked:
                    print('Waiting, as {} is already being downloaded...'.
                          format(url))
                was_locked = True
                time.sleep(0.1)

    if not was_locked:
        if os.path.getsize(filename) > 0:
            print('Not downloading {} as {} already present'.format(
                url, filename))
        else:
            print('Downloading {} to {} ...'.format(url, filename))
            urllib.request.urlretrieve(url, filename)

    # release lock and return
    fcntl.flock(fp, fcntl.LOCK_UN)
    return filename
