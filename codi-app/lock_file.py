import os
import time
import psutil

def check_and_kill(file):
    pid = None
    try:
        f = open(file, 'r')
        pidstr = f.read()
        f.close()
        pid = int(pidstr)
    except Exception as e:
        return False

    print("Killing PID:",pid)
    count = 0
    while pid > 0 and psutil.pid_exists(pid):
        try:
            os.kill(pid, count)
            if count == 9:
                os.waitpid(pid, 0)
            count = count + 1
            time.sleep(1)
            print("killed",count)
        except OSError:
            print("can't deliver signal", count, "to", pid)
            pid = 0
    os.remove(file)
    return count > 0

def lock(file):
    pidfd = os.open(file, os.O_CREAT|os.O_WRONLY|os.O_EXCL)
    os.write(pidfd, str(os.getpid()).encode())
    os.close(pidfd)

def remove(file):
    print('removed pidfile %s' % file)
    os.remove(file)
