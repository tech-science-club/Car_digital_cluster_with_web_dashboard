#Example of CAN bus Reader based on PCANBasic.py

from PCANBasic import *
from threading import Thread

class Dash_Board(Thread):
    rpm = 0
    speed = 0
    t = 21
    fuel = 0
    consm = 0
    arrow_angle = 0
    widget_name = None
    widget_yaxes_name = None
    arrow_speed = 0
    arrow_rpm = 0
    lat = 0
    lon = 0
    num = 0
    line = 0
    gps_message = None
    at_response = None
    msg = None

class TimerRepeater(object):
    """
    A simple timer implementation that repeats itself
    """

    ## Constructor
    def __init__(self, name, interval, target):
        """
        Creates a timer.

        Parameters:
            name = name of the thread
            interval = interval in second between execution of target
            target = function that is called every 'interval' seconds
        """
        # define thread and stopping thread event
        self._name = name
        self._thread = None
        self._event = None
        # initialize target
        self._target = target
        # initialize timer
        self._interval = interval

        # Runs the thread that emulates the timer

    #
    def _run(self):
        """
        Runs the thread that emulates the timer.

        Returns:
            None
        """
        while not self._event.wait(self._interval):
            self._target()

            # Starts the timer

    #
    def start(self):
        """
        Starts the timer

        Returns:
            None
        """
        # avoid multiple start calls
        if (self._thread == None):
            self._event = threading.Event()
            self._thread = threading.Thread(None, self._run, self._name)
            self._thread.start()

            # Stops the timer

    #
    def stop(self):
        """
        Stops the timer

        Returns:
            None
        """
        if (self._thread != None):
            self._event.set()
            self._thread.join()
            self._thread = None

class Read_bus_data(Thread):

    def __init__(self, **kwargs):
        Thread.__init__(self)
        self.line = 0

        # Timerinterval (ms) for reading
        self.TimerInterval = 100
        # self.data_queue = data_queue
        self.PcanHandle = PCAN_USBBUS1
        self.Bitrate = PCAN_BAUD_500K

        self.m_objTimer = TimerRepeater("ReadMessages", 0.0001, self.Read_data)
        self.m_objTimer.start()

        self.m_objPCANBasic = PCANBasic()
        self.stsResult = self.m_objPCANBasic.Initialize(self.PcanHandle, self.Bitrate)

    def Read_data(self):
        self.ReadMessages()

    def ReadMessages(self):
        Dash_Board.line += 1
        # print(self.line)
        try:
            self.Result = self.m_objPCANBasic.Read(self.PcanHandle)

            msg = self.Result[1]
            timestamp = self.Result[2]
            Dash_Board.msg = list(msg.DATA)

            if msg.ID == 0x316 and msg is not None:
                Dash_Board.rpm = msg.DATA[3] * 7000 / 110
                Dash_Board.arrow_rpm = Dash_Board.rpm
                Dash_Board.rpm = round(Dash_Board.rpm / 50) * 50

            elif msg.ID == 0x1F1 and msg is not None:
                Dash_Board.speed = msg.DATA[4] * 220 / 100
                Dash_Board.arrow_speed = Dash_Board.speed * 260 / 220

            elif msg.ID == 0x0A0 and msg is not None:
                Dash_Board.t = msg.DATA[1] - 40

            elif msg.ID == 0x0A1 and msg is not None:
                Dash_Board.consm = msg.DATA[4] * 20 / 100

            elif msg.ID == 0x0350 and msg is not None:
                Dash_Board.fuel = msg.DATA[3] * 0.75


            # to print out upcoming data uncoment bellow
            # print(f"{Dash_Board.line}: --> {Dash_Board.rpm} {Dash_Board.speed} {Dash_Board.t} {Dash_Board.boost} {Dash_Board.fuel}")
        except Exception as e:
            print("eror: ", e)
            self.Read_data()