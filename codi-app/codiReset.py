#!/usr/bin/env python3
import time
import lock_file

def stm32_hardware_reset():
    print("Reset STM32 1")
    with open('/proc/AEON_RESET_STM32', 'w') as f:
        f.write("1")
    time.sleep(1)
    print("Reset STM32 0")
    with open('/proc/AEON_RESET_STM32', 'w') as f:
        f.write("0")
    time.sleep(4)


def stm32_out_of_download_mode():
    print("Out of download mode")
    with open('/proc/AEON_STM32_DL_FW', 'w') as f:
        f.write("0")

lock = "/tmp/.codi.lock"
killed = lock_file.check_and_kill(lock)
lock_file.lock(lock)

stm32_hardware_reset()
stm32_out_of_download_mode()
