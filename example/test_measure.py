# Copyright (c) 2024 Ryohei Niwase <rniwase@lila.cs.tsukuba.ac.jp>
# SPDX-License-Identifier: BSD-2-Clause

import time
from hioki3334 import HIOKI3334

def print_measure(m, with_integ=False):
    print(f"  Voltage: {m['V']} [V]")
    print(f"  Current: {m['A']} [A]")
    print(f"  Voltage waveform peak: {m['VPK']} [V]")
    print(f"  Current waveform peak: {m['APK']} [A]")
    print(f"  Active power: {m['W']} [W]")
    print(f"  Apparent power: {m['VA']} [VA]")
    print(f"  Power factor: {m['PF']}")
    print(f"  Frequency: {m['FREQ']} [Hz]")
    if with_integ:
        print(f"  Positive current integration: {m['PAH']} [Ah]")
        print(f"  Negative current integration: {m['MAH']} [Ah]")
        print(f"  Total current integration: {m['AH']} [Ah]")
        print(f"  Positive power integration: {m['PWH']} [Wh]")
        print(f"  Negative power integration: {m['MWH']} [Wh]")
        print(f"  Total power integration: {m['WH']} [Wh]")
        print(f"  Integration: {m['APK']} [sec.]")


if __name__ == "__main__":
    with HIOKI3334(device="/dev/ttyUSB0") as hioki:
        print("Reset HIOKI 3334")
        hioki.reset()
        time.sleep(1.)

        print("Identify: {}".format(hioki.identify()))

        print("Execute self-test")
        assert hioki.self_test() == 0

        print("Set rectifier mode to AC/DC")
        hioki.rectifier(mode="acdc")

        print("Set averaging count to 1")
        hioki.averaging(1)

        print("Set voltage/current range to AUTO")
        hioki.voltage_range(range="auto")
        hioki.current_range(range="auto")
        time.sleep(1)

        print("Reset peak-hold")
        hioki.reset_peak_hold()

        print("Acquire measurements immediately")
        print_measure(hioki.measure())

        print("Reset integration")
        hioki.integrate(state="reset")

        print("Reset peak-hold")
        hioki.reset_peak_hold()

        print("Start integration")
        hioki.integrate(state="start")

        print("Wait 10 sec.")
        time.sleep(10.)

        print("Stop integration")
        hioki.integrate(state="stop")

        print("Acquire measurements including integration")
        print_measure(hioki.measure(), with_integ=True)

        print("Reset integration")
        hioki.integrate(state="reset")
