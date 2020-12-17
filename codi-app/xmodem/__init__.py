'''
=======================================
 Modified YMODEM file transfer protocol
=======================================

.. $Id$

This is a implementation of YMODEM as used on the Cosmo Communicator.

Data flow example
=================

Here is a sample of the data flow, sending a 3-block message.

Batch Transmission Session (1 file - not tested with more than one)
-------------------------------------------------------------------

::

    SENDER                                      RECEIVER
                                            <-- C (command:rb)
    SOH 00 FF foo.c NUL[123] CRC CRC        -->
                                            <-- ACK
    SOH 01 FE Data[1024] CRC CRC            --> (probably received garbled)
                                            <-- C
    SOH 01 FE Data[1024] CRC CRC (resend)   --> (starts flash erase)
                                            <-- (empty read timed out)
                                            <-- (empty read timed out)
                                            <-- (empty read timed out)
                                            <-- C
    SOH 01 FE Data[1024] CRC CRC (resend)   -->
                                            <-- ACK
    SOH 02 FC Data[1024] CRC CRC            --> (probably received garbled)
                                            <-- C
    SOH 02 FC Data[1024] CRC CRC (resend)   -->
                                            <-- ACK
    SOH 03 FB Data[1000] CPMEOF[24] CRC CRC  -->
                                            <-- ACK
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- C
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- C
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- C
    EOT                                     -->
    EOT                                     -->
    EOT                                     -->
                                            <-- ACK

'''
from __future__ import division, print_function

__author__ = 'Wijnand Modderman <maze@pyth0n.org>'
__copyright__ = ['Copyright (c) 2010 Wijnand Modderman',
                 'Copyright (c) 1981 Chuck Forsberg',
                 'Copyright (c) 2016 Michael Tesch']
__license__ = 'MIT'
__version__ = '0.4.5'

import platform
import logging
import time
import sys
import os

# Protocol bytes
NUL = b'\x00'
SOH = b'\x01'
STX = b'\x02'
EOT = b'\x04'
ACK = b'\x06'
ACK2 = b'\x86'
DLE = b'\x10'
NAK = b'\x15'
CAN = b'\x18'
CAN2 = b'\x98'
CRC = b'C' #0x43
CRC2 = b'\xc3'
CRC3 = b'\x83'
ABT = b'a' #0x61 - flash fail - abort

class YMODEM(object):
    '''
    YMODEM Protocol handler, expects two callables which encapsulate the read
        and write operations on the underlying stream.

    Example functions for reading and writing to a serial line:

    >>> import serial
    >>> from xmodem import YMODEM
    >>> ser = serial.Serial('/dev/ttyUSB0', timeout=0) # or whatever you need
    >>> modem = YMODEM(ser)


    :param ser: serial port to read from or write to.
    :type getc: class
    :type mode: string
    :param pad: Padding character to make the packets match the packet size
    :type pad: char

    '''

    # crctab calculated by Mark G. Mendel, Network Systems Corporation
    crctable = [
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
        0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
        0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
        0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
        0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
        0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
        0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
        0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
        0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
        0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
        0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
        0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
        0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
        0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
        0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
        0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
        0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
        0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
        0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
        0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
        0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
        0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
        0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
        0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
        0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
        0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
        0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
        0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0,
    ]

    def __init__(self, ser, pad=b'\x1a'):
        self.ser = ser
        self.pad = pad
        self.log = logging.getLogger('codiUpdate')

    def abort(self, count=2, timeout=60):
        '''
        Send an abort sequence using CAN bytes.

        :param count: how many abort characters to send
        :type count: int
        :param timeout: timeout in seconds
        :type timeout: int
        '''
        for _ in range(count):
            self.ser.write(CAN)

    def send(self, filename, retry=20, timeout=60, quiet=False, callback=None):
        '''
        Send a stream via the YMODEM protocol.

            >>> print(modem.send('filename'))
            True

        Returns ``True`` upon successful transmission or ``False`` in case of
        failure.

        :param stream: The stream object to send data from.
        :type stream: stream (file, etc.)
        :param retry: The maximum number of times to try to resend a failed
                      packet before failing.
        :type retry: int
        :param timeout: The number of seconds to wait for a response before
                        timing out.
        :type timeout: int
        :param quiet: If True, write transfer information to stderr.
        :type quiet: bool
        :param callback: Reference to a callback function that has the
                         following signature.  This is useful for
                         getting status updates while a ymodem
                         transfer is underway.
                         Expected callback signature:
                         def callback(total_packets, success_count, error_count, total)
        :type callback: callable
        '''

        # initialize protocol
        packet_size = 1024

        self.log.debug('Begin start sequence, packet_size=%d', packet_size)
        error_count = 0
        crc_mode = 0
        cancel = 0
        while True:
            char = self.ser.read(1)
            if char:
                if char == NAK:
                    self.log.debug('standard checksum requested (NAK).')
                    crc_mode = 0
                    break
                elif char == CRC:
                    self.log.debug('16-bit CRC requested (CRC).')
                    crc_mode = 1
                    break
                elif char == CAN or char == CAN2:
                    if not quiet:
                        print('received CAN', file=sys.stderr)
                    if cancel:
                        self.log.info('Transmission canceled: received 2xCAN '
                                      'at start-sequence')
                        return False
                    else:
                        self.log.debug('cancellation at start sequence.')
                        cancel = 1
                else:
                    self.log.error('send error: expected NAK, CRC, or CAN; '
                                   'got %r', char)

            error_count += 1
            if error_count > retry:
                self.log.info('send error: error_count reached %d, '
                              'aborting.', retry)
                self.abort(timeout=timeout)
                return False

        # send data
        error_count = 0
        success_count = 0
        total_packets = 0
        total = 0
        header_sent = False
        sequence = 0
        stream = None
        while True:
            # build packet
            if not header_sent:
                # send packet sequence 0 containing:
                #  Filename Length [Modification-Date [Mode [Serial-Number]]]
                stream = open(filename, 'rb')
                stat = os.stat(filename)
                data = os.path.basename(filename).encode() + NUL + str(stat.st_size).encode()
                self.log.debug('ymodem sending : "%s" len:%d', filename, stat.st_size)

                if len(data) <= 128:
                    header_size = 128
                else:
                    header_size = 1024

                header = self._make_send_header(header_size, sequence)
                data = data.ljust(header_size, NUL)
                checksum = self._make_send_checksum(crc_mode, data)
                header_sent = True
                total = (stat.st_size / packet_size) + 1
            else:
                # normal data packet
                data = stream.read(packet_size)
                if not data:
                    # end of stream
                    self.log.debug('send: at EOF')
                    break
                total_packets += 1

                header = self._make_send_header(packet_size, sequence)
                data = data.ljust(packet_size, self.pad)
                checksum = self._make_send_checksum(crc_mode, data)

            # emit packet & get ACK
            self.ser.write(header + data + checksum)

            while True:
                char = self.ser.read(1)
                if char == CRC or char == CRC2 or char == CRC3:
                    if self.ser.in_waiting == 0:
                        self.log.debug('re-send: block %d, pks: %d', sequence, packet_size)
                        self.ser.write(header + data + checksum)
                    else:
                        rubbish = self.ser.read(self.ser.in_waiting-1)
                        self.log.error('got NAK rubbish %r for block %d', rubbish, sequence)
                    continue
                if char == ACK or char == ACK2 or char == NAK:
                    success_count += 1
                    if callable(callback):
                        callback(total_packets, success_count, error_count, total)
                    error_count = 0
                    if char == NAK:
                        rubbish = self.ser.read(1024)
                        self.log.error('got NAK rubbish %r for block %d', rubbish, sequence)
                        rubbish = self.ser.read(1024)
                        self.log.error('got NAK rubbish %r for block %d', rubbish, sequence)
                        rubbish = self.ser.read(1024)
                        self.log.error('got NAK rubbish %r for block %d', rubbish, sequence)
                        rubbish = self.ser.read(1024)
                        self.log.error('got NAK rubbish %r for block %d', rubbish, sequence)
                    break
                if char == ABT:
                    self.log.debug('got abort')
                    return False

                self.log.error('send error: expected CRC|ACK; got %r for block %d',
                               char, sequence)
                error_count += 1
                if callable(callback):
                    callback(total_packets, success_count, error_count, total)
                if error_count > retry:
                    # excessive amounts of retransmissions requested,
                    # abort transfer
                    self.log.error('send error: Unexpected received %d times, '
                                   'aborting.', error_count)
                    self.abort(timeout=timeout)
                    return False

            # keep track of sequence
            sequence = (sequence + 1) % 0x100

        # emit EOT and get corresponding ACK
        while True:
            self.log.debug('sending EOT, awaiting ACK')
            # end of transmission
            self.ser.write(EOT)
            self.ser.write(EOT)
            self.ser.write(EOT)

            # An ACK should be returned
            char = self.ser.read(1)
            if char == ACK:
                break
            else:
                self.log.error('send error: expected ACK; got %r', char)
                error_count += 1
                if error_count > retry:
                    self.log.warning('EOT was not ACKd, aborting transfer')
                    self.abort(timeout=timeout)
                    return False

        self.log.info('Transmission successful (ACK received).')
        stream.close()
        return True

    def _make_send_header(self, packet_size, sequence):
        assert packet_size in (128, 1024), packet_size
        _bytes = []
        if packet_size == 128:
            _bytes.append(ord(SOH))
        elif packet_size == 1024:
            _bytes.append(ord(STX))
        _bytes.extend([sequence, 0xff - sequence])
        return bytearray(_bytes)

    def _make_send_checksum(self, crc_mode, data):
        assert crc_mode is 1
        _bytes = []
        if crc_mode:
            crc = self.calc_crc(data)
            _bytes.extend([crc >> 8, crc & 0xff])
        return bytearray(_bytes)

    def calc_crc(self, data, crc=0):
        '''
        Calculate the Cyclic Redundancy Check for a given block of data, can
        also be used to update a CRC.

            >>> crc = modem.calc_crc('hello')
            >>> crc = modem.calc_crc('world', crc)
            >>> hex(crc)
            '0xd5e3'

        '''
        for char in bytearray(data):
            crctbl_idx = ((crc >> 8) ^ char) & 0xff
            crc = ((crc << 8) ^ self.crctable[crctbl_idx]) & 0xffff
        return crc & 0xffff



