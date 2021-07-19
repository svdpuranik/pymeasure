#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2021 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range


from pymeasure.adapters import VISAAdapter


class Keysight3446xA(Instrument):
    """ Represents the Keysight 3446xA Digital Multimeter
    interface for interacting with the instrument.

    .. code-block:: python

    """
    ###############
    # Current (A) #
    ###############
    current_dc = Instrument.ask(":MEASure:CURRent:DC",
        """ Reads a setting current in Amps. """
     )

    current_ac = Instrument.ask(":MEASure:CURRent:AC",
        """ Reads a setting current in Amps. """
     )

    ###############
    # Voltage (V) #
    ###############
    voltage_dc = Instrument.measurement(":MEASure:VOLTage:DC",
        """ Reads a DC voltage measurement in Volts. """
     )

    voltage_ac = Instrument.measurement(":MEASure:VOLTage:AC",
        """ Reads a DC voltage measurement in Volts. """
     )

    ##############
    #_status (0/1) #
    ##############
    _status = Instrument.measurement(":OUTP?",
        """ Read power supply current output status. """,
    )

    def enable(self):
        """ Enables the flow of current.
        """
        self.write(":OUTP 1")

    def disable(self):
        """ Disables the flow of current.
        """
        self.write(":OUTP 0")

    def is_enabled(self):
        """ Returns True if the current supply is enabled.
        """
        return bool(self._status)

    def __init__(self, adapter, **kwargs):
        super(Keysight3446xA, self).__init__(
            adapter, "Keysight 3446xA digital multimeter", **kwargs
        )
        # Set up data transfer format
        if isinstance(self.adapter, VISAAdapter):
            self.adapter.config(
                is_binary=False,
                datatype='float32',
                converter='f',
                separator=','
            )

    def check_errors(self):
        """ Read all errors from the instrument."""
        while True:
            err = self.values(":SYST:ERR?")
            if int(err[0]) != 0:
                errmsg = "Keysight N5767A: %s: %s" % (err[0],err[1])
                log.error(errmsg + '\n')
            else:
                break
