# Copyright (c) 2024 Ryohei Niwase <rniwase@lila.cs.tsukuba.ac.jp>
# SPDX-License-Identifier: BSD-2-Clause

import serial

class HIOKI3334():
    def __init__(self, device="/dev/ttyUSB0", timeout=10):
        self.device = device
        self.timeout = timeout

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.close()

    def open(self):
        self.ser = serial.Serial(self.device, 9600, timeout=self.timeout)

    def close(self):
        self.ser.close()

    def send(self, cmd):
        self.ser.write(cmd.encode())
        self.ser.write(b"\r\n")
        self.ser.flush()

    def recv(self):
        res = self.ser.readline()
        res = res[:-2].decode()
        return res

    def identify(self):
        self.send("*IDN?")
        return self.recv()

    def reset(self):
        self.send("*RST")

    def self_test(self):
        self.send("*TST?")
        return int(self.recv())

    def averaging(self, average=None):
        if average in [1, 2, 5, 10, 25, 50, 100]:
            self.send(":AVERAGING {}".format(str(average)))
        elif average is None:
            pass
        else:
            raise

        self.send(":AVERAGING?")
        res = int(self.recv().split(" ")[1])
        if res in [1, 2, 5, 10, 25, 50, 100]:
            return res
        else:
            raise

    def hold(self, hold=None):
        if hold is not None:
            self.send(":HOLD {}".format("ON" if hold else "OFF"))

        self.send(":HOLD?")
        res = self.recv().split(" ")[1]
        if res in ["ON", "OFF"]:
            return res == "ON"
        else:
            raise

    def peak_hold(self, hold=None):
        if hold is not None:
            self.send(":PEAKHOLD {}".format("ON" if hold else "OFF"))

        self.send(":PEAKHOLD?")
        res = self.recv().split(" ")[1]
        if res in ["ON", "OFF"]:
            return res == "ON"
        else:
            raise

    def reset_peak_hold(self):
        self.send(":PEAKHOLD RESET")

    def rectifier(self, mode=None):
        if mode in ["acdc", "dc", "ac"]:
            self.send(":RECTIFIER {}".format(mode.upper()))

        self.send(":RECTIFIER?")
        res = self.recv().split(" ")[1]
        if res in ["ACDC", "DC", "AC"]:
            return res.lower()
        else:
            raise

    def voltage_range(self, range=None):
        if range in [15, 30, 150, 300]:
            self.send(":VOLTAGE:RANGE {};AUTO OFF".format(str(range)))
        elif range == "auto":
            self.send(":VOLTAGE:AUTO ON")
        elif range == None:
            pass
        else:
            raise

        params = dict()

        self.send(":VOLTAGE?")
        res = self.recv()
        res = res.split(";")
        for r in res:
            if ":VOLTAGE:RANGE" in r:
                params["range"] = int(r.split(" ")[1])
            if "AUTO" in r:
                res_auto = r.split(" ")[1]
                if res_auto == "ON":
                    params["auto"] = True
                elif res_auto == "OFF":
                    params["auto"] = False
                else:
                    raise

        return params

    def current_range(self, range=None):
        if range in [0.1, 0.3, 1.0, 3.0, 10.0, 30.0]:
            self.send(":CURRENT:RANGE {};AUTO OFF".format(str(range)))
        elif range == "auto":
            self.send(":CURRENT:AUTO ON")
        elif range == None:
            pass
        else:
            raise

        params = dict()

        self.send(":CURRENT?")
        res = self.recv()
        res = res.split(";")
        for r in res:
            if ":CURRENT:RANGE" in r:
                params["range"] = float(r.split(" ")[1])
            if "AUTO" in r:
                res_auto = r.split(" ")[1]
                if res_auto == "ON":
                    params["auto"] = True
                elif res_auto == "OFF":
                    params["auto"] = False
                else:
                    raise

        return params

    def integrate(self, state=None):
        if state in ["start", "stop", "reset"]:
            self.send(":INTEGRATE:STATE {}".format(state.upper()))
        elif state is None:
            pass
        else:
            raise

        self.send("INTEGRATE:STATE?")
        res = self.recv()
        res = res.split(" ")[1]
        if res in ["START", "STOP", "RESET"]:
            return res.lower()
        else:
            raise

    def measure(self):
        self.send(":MEASURE? V,A,W,VA,PF,FREQ,PAH,MAH,AH,PWH,MWH,WH,VPK,APK,TIME")
        res = self.recv().split(";")
        measures = dict()
        for r in res:
            m = r.split(" ")
            if m[0] == "TIME":
                hms = m[1].split(",")
                measures["TIME"] = (int(hms[0]) * 60 * 60) + (int(hms[1]) * 60) + int(hms[2])
            else:
                if m[1] == "+999.99E+9":
                    measures[m[0]] = float("inf")
                elif m[1] == "-999.99E+9":
                    measures[m[0]] = float("-inf")
                else:
                    measures[m[0]] = float(m[1])

        return measures
