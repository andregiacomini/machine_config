import serial
from serial.tools import list_ports
from tkinter import *
from tkinter import messagebox as tkMessageBox
import json
import time

root = Tk()
root.iconbitmap(default='r2d2.ico')

class SerialConnector():
    VID = 0x0403
    PID = 0x6001
    connected = False

    ser = serial.Serial(timeout=1)

    def get_port(self):
        device_list = list_ports.comports()
        for device in device_list:
            if device.vid is not None or device.pid is not None:
                if ('{:04X}'.format(self.VID) == '{:04X}'.format(device.vid) and
                    '{:04X}'.format(self.PID) == '{:04X}'.format(device.pid)):
                    port = device.device
                    return port
                    break
                port = None
                return port

    def connect(self):
        self.ser.baudrate = 115200
        self.ser.port = self.get_port()
        if self.ser.port is None:

            print("Nenhum device conectado")
        else:
            try:
                self.ser.open()
            except SerialConnector as e:
                print (str(e))
            self.ser.setRTS(0)
            self.ser.setDTR(0)
            self.ser.setDTR(1)
            self.ser.setDTR(0)

    def disconnect(self):
        self.ser.close()

    def write_serial(self, method="", arg1="", arg2=""):

        msg = "{\"M\":\"%s\",\"K\":\"%s\"" % (method, arg1)
        if arg2 is not "":
            msg += ",\"V\":\"%s\"}" % arg2
        else:
            msg += "}"
        if(len(msg)>50):
            raise Exception('Message too big')
        else:
            msg = msg + (50-(len(msg)))*'*'
            print(msg)
            self.ser.write(msg.encode())

    def read_serial(self):
        line = self.ser.readline();
        return line

    @property
    def is_connected(self):
        if self.ser.is_open:
            return "Conectado na Porta %s" % self.ser.port
        else:
            return "Desconectado"


class GUI:
    ser = SerialConnector()
    parameters = dict()
    entries = []
    lbl_entries = []
    line_counter = int()
    def __init__(self, master):
        self.master = master
        master.title("Configurador")
        master.resizable(0, 0)  # Don't allow resizing in the x or y direction

        self.lbl_isConnected = Label(master, text="Desconectado")
        self.lbl_isConnected.grid(column=0, row=0)

        self.btn_connect = Button(master, text="Conectado", command=self.connect, width=20,)
        self.btn_connect.grid(column=0, row=1)

        self.btn_disconnect = Button(master, text="Desconectar", command=self.disconnect, width=20)
        self.btn_disconnect.grid(column=1, row=1)

        self.btn_read = Button(master, text="Ler Flash", command=self.read_parameters, width=20)
        self.btn_read.grid(column=0, row=2)

        self.btn_write = Button(master, text="Escrever Flash", command=self.write_parameters, width=20)
        self.btn_write.grid(column=1, row=2)

        self.update_interface()

    def update_interface(self):
        self.lbl_isConnected.config(text=self.ser.is_connected)

    def connect(self):
        self.ser.connect()
        self.update_interface()

    def disconnect(self):
        for n in self.entries:
            n.destroy()
        del self.entries[:]
        for n in self.lbl_entries:
            n.destroy()
        del self.lbl_entries[:]
        self.parameters.clear()
        self.ser.disconnect()
        self.update_interface()

    def read_parameters(self):
        self.line_counter = 0
        self.ser.write_serial("R", "0", "0")
        if self.ser.is_connected != "Desconectado":
            del self.entries[:]
            del self.lbl_entries[:]
            while 1:
                line = self.ser.read_serial()
                j = json.loads(line)
                if "END" in j:
                    break

                label = Label(self.master, width=20)
                label.grid(column=0, row=3 + self.line_counter)
                entry = Entry(self.master, width=20, justify=RIGHT)
                entry.grid(column=1, row=3 + self.line_counter)
                self.lbl_entries.append(label)
                self.entries.append(entry)


                for x in j:
                    label['text'] = str(x)
                    entry.insert(0, str(j[x]))

                self.line_counter += 1
                print(line)
                self.update_interface()

    def write_parameters(self):
        writting_ok = bool()
        if self.ser.is_connected != "Desconectado":
            if self.line_counter > 0:
                for n in range(len(self.entries)):
                    self.ser.write_serial("W", self.lbl_entries[n].cget('text'), self.entries[n].get())
                    time.sleep(0.01)
                    line = self.ser.read_serial()
                    j = json.loads(line)
                    writting_ok = 1
                    print(line)
                    if "SUCCESS" not in j:
                        writting_ok = 0
                        break

            if writting_ok:
                tkMessageBox.showinfo("Info","Flash gravada com sucesso!")
            else:
                msg = "Erro ao gravar Flash: " + j[self.lbl_entries[n].cget('text')]
                tkMessageBox.showerror("Erro", msg)

gui = GUI(root)
root.mainloop()


