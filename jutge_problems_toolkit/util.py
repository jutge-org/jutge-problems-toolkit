# ----------------------------------------------------------------------------
# (c) Jordi Petit 2006-2009
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Importations
# ----------------------------------------------------------------------------

import os
import sys
import time
import fcntl
import shutil
import glob
import tarfile
import base64
import stat
import tempfile
import resource
import subprocess
import socket
import yaml
import hashlib


# ----------------------------------------------------------------------------
# Environment
# ----------------------------------------------------------------------------


def get_username():
    return os.getenv("USER")


def get_hostname():
    return socket.gethostname()


# ----------------------------------------------------------------------------
# Utilities for lists
# ----------------------------------------------------------------------------

def intersection(a, b):
    return filter(lambda x: x in a, b)

# ----------------------------------------------------------------------------
# Utilities for general directories
# ----------------------------------------------------------------------------


def read_file(name):
    """Returns a string with the contents of the file name."""
    f = open(name)
    r = f.read()
    f.close()
    return r


def write_file(name, txt=""):
    """Writes the file name with contents txt."""
    f = open(name, "w")
    f.write(txt)
    f.close()


def append_file(name, txt=""):
    """Adds to file name the contents of txt."""
    f = open(name, "a")
    f.write(txt)
    f.close()


def del_file(name):
    """Deletes the file name. Does not complain on error."""
    try:
        os.remove(name)
    except OSError:
        pass


def file_size(name):
    """Returns the size of file name in bytes."""
    return os.stat(name)[6]


def tmp_dir():
    """Creates a temporal directory and returns its name."""
    return tempfile.mkdtemp('.dir', get_username() + '-')


def tmp_file():
    """Creates a temporal file and returns its name."""
    return tempfile.mkstemp()[1]


def file_exists(name):
    """Tells whether file name exists."""
    return os.path.exists(name)


def copy_file(src, dst):
    """Copies a file from src to dst."""
    shutil.copy(src, dst)


def copy_dir(src, dst):
    """Recursively copy an entire directory tree rooted at src to dst."""
    shutil.copytree(src, dst)


def move_file(src, dst):
    """Recursively move a file or directory to another location."""
    shutil.move(src, dst)


# ----------------------------------------------------------------------------
# Utilities for yml files
# ----------------------------------------------------------------------------


def print_yml(inf):
    print(yaml.dump(inf, indent=4, width=1000, default_flow_style=False))


def write_yml(path, inf):
    yaml.dump(inf, open(path, "w"), indent=4,
              width=1000, default_flow_style=False)


def read_yml(path):
    return yaml.load(open(path, 'r'), Loader=yaml.FullLoader)


# ----------------------------------------------------------------------------
# Utilities for properties files
# ----------------------------------------------------------------------------


def read_props(path):
    """Returns a dictionary with the properties of file path."""
    dic = {}
    f = open(path)
    for l in f.readlines():
        k, v = l.split(":", 1)
        dic[k.strip()] = v.strip()
    return dic


def write_props(path, inf):
    """Writes to file path the properties of file inf."""
    t = ""
    for k, v in inf.iteritems():
        t += k + ": " + v + "\n"
    write_file(path, t)


# ----------------------------------------------------------------------------
# Utilities for tar/tgz files
# ----------------------------------------------------------------------------


def create_tar(name, filenames, path=None):
    """Creates a tar file name with the contents given in the list of filenames.
    Uses path if given."""
    if name == "-":
        tar = tarfile.open(mode="w|", fileobj=sys.stdout)
    else:
        tar = tarfile.open(name, "w")
    if path:
        cwd = os.getcwd()
        os.chdir(path)
    for x in filenames:
        tar.add(x)
    if path:
        os.chdir(cwd)
    tar.close()


def create_tgz(name, filenames, path=None):
    """Creates a tgz file name with the contents given in the list of filenames.
    Uses path if given."""
    if name == "-":
        tar = tarfile.open(mode="w|gz", fileobj=sys.stdout)
    else:
        tar = tarfile.open(name, "w:gz")
    if path:
        cwd = os.getcwd()
        os.chdir(path)
    for x in filenames:
        tar.add(x)
    if path:
        os.chdir(cwd)
    tar.close()


def extract_tar(name, path):
    """Extracts a tar file in the given path."""
    if name == "-":
        tar = tarfile.open(mode="r|", fileobj=sys.stdin)
    else:
        tar = tarfile.open(name)
    for x in tar:
        tar.extract(x, path)
    tar.close()


def extract_tgz(name, path):
    """Extracts a tgz file in the given path."""
    if name == "-":
        tar = tarfile.open(mode="r|gz", fileobj=sys.stdin)
    else:
        tar = tarfile.open(name, "r:gz")
    for x in tar:
        tar.extract(x, path)
    tar.close()


def get_from_tgz(tgz, name):
    """Returns the contents of file name inside a tgz or tar file."""
    tar = tarfile.open(tgz)
    f = tar.extractfile(name)
    r = f.read()
    f.close()
    tar.close()
    return r


# ----------------------------------------------------------------------------
# Utilities for directories
# ----------------------------------------------------------------------------


def del_dir(path):
    """Deletes the directory path. Does not complain on error."""
    try:
        shutil.rmtree(path)
    except OSError:
        pass


def mkdir(path):
    """Makes the directory path. Does not complain on error."""
    try:
        os.makedirs(path)
    except OSError:
        pass


# ----------------------------------------------------------------------------
# Utilities for dates and times
# ----------------------------------------------------------------------------


def current_year():
    """Returns a string with the current year."""
    return time.strftime("%Y")


def current_time():
    """Returns a string with out format for times."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def current_date():
    """Returns a string with out format for dates."""
    return time.strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------
# I THINK THE THE FOLLOWING FUNCTIONS ARE DEPRECATED.
# IF NOT I HAVE TO MOVE THEM TO OTHER PLACES.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Others
# ----------------------------------------------------------------------------


def myhash(s):
    """Returns an hexadecimal hash of s."""
    h = hashlib.md5()
    h.update(s)
    return h.hexdigest()


def system(cmd):
    """As os.system(cmd) but writes cmd."""
    print(cmd)
    return os.system(cmd)


def cd_system(path, cmd):
    """As os.system(cmd) but executes from directory path."""
    print(cmd)
    pushd(path)
    r = os.system(cmd)
    popd()
    return r


def command(cmd):
    """As os.system(cmd) but returns stdout as an string."""
    return subprocess.getoutput(cmd)


def myprint(msg):
    """Print the message msg in log format and flushes."""
    print(current_time() + " - " + msg)
    sys.stderr.flush()
    sys.stdout.flush()


# ----------------------------------------------------------------------------
# Utilities for deamons
# ----------------------------------------------------------------------------


def deamon_exec(func, msg):
    """
        Executes function func (without arguments) in a daemon process.
        If all goes well, writes message msg and the PID of the daemon.
    """

    pid = os.fork()
    if pid > 0:
        os._exit(0)
    os.setsid()
    pid = os.fork()
    if pid > 0:
        print(msg, pid)
        os._exit(0)

    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass

    func()
    os._exit(0)


# ----------------------------------------------------------------------------
# A class to lock files
# ----------------------------------------------------------------------------

class lock:

    def __init__(self, filename, shared=False, timeout=5, step=0.2):
        """
        Create a lock object with a file filename

        timeout is the time in seconds to wait before timing out, when
        attempting to acquire the lock.
        step is the number of seconds to wait in between each attempt to
        acquire the lock.

        """
        self.locked = False
        t = 0
        while True:
            t += step
            self.lockfile = open(filename, "w")
            try:
                if shared:
                    fcntl.flock(self.lockfile.fileno(),
                                fcntl.LOCK_SH | fcntl.LOCK_NB)
                else:
                    fcntl.flock(self.lockfile.fileno(),
                                fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                if t < timeout:
                    time.sleep(step)
                else:
                    raise IOError("Failed to acquire lock on %s" % filename)
            else:
                self.locked = True
                return

    def unlock(self):
        """
            Release the lock.
        """
        if self.locked:
            fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_UN)
            self.locked = False
            self.lockfile.close()

    def __del__(self):
        """
            Auto unlock when object is deleted.
        """
        self.unlock()
