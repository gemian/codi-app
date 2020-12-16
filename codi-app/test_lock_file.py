#!/usr/bin/env python3
import lock_file
import os
import time

lock = "/tmp/test.lock"
try:
    os.remove(lock)
    print("Test file was present, unexpected")
except FileNotFoundError:
    print("Test file not present as expected")

killed = lock_file.check_and_kill(lock)
print("Should be False:", killed)

pid = os.fork()
if pid == 0:
    #lock and keep spinning forever
    lock_file.lock(lock)
    while True:
        time.sleep(100)
print("Child running PID:",pid)
time.sleep(0.1)
killed = lock_file.check_and_kill(lock)
print("Should be True:", killed)

# Create stale lock file
pidfd = os.open(lock, os.O_CREAT|os.O_WRONLY|os.O_EXCL)
os.write(pidfd, "123456789".encode())
os.close(pidfd)

print("Expect: can't deliver signal 1&2 to 123456789")
killed = lock_file.check_and_kill(lock)
print("Should be False:", killed)
lock_file.lock(lock)
