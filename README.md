Car Dashboard with relevant information from CAN bus.

Depiction of the vehicle CAN information on the gadget's screen in the form of Digital Cluster as it is so popular nowadays 
on modern cars.

To go further and to bring something new in this area was decided to design and embed into the car system which can 
read CAN bus, depict it on its screen and pass data to the web and depict that information on web page having correspondent 
data in the database.
It might be relevant if you want to keep a track on your car usage and have its statistic data 

The working platform to embed idea into the life was chosen Raspberry pi 4 with correspondent
features and possibilities to have a screen with high resolution.

link: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/

![](rpi4.png)

To communicate with CAN bus on the vehicle was chosen CANable adapter. Easy to use, cheap and can interact with CANViewer
and Python-can library

![](CANable.jpg)

To send data via GSM I have been using A9GTkinter module
link: https://docs.ai-thinker.com/gprs 

![](1.webp)

To read GPS data I have chosen well known and good recommended Neo6m GPS tracker:

![](neo6m.webp)

In the case to debug our CAN module and check it's work ability I have made a debug module from Arduino Mega and MCP2515.
It can generate random CAN messages and send it to the our CANable module
![](ATMega2560+MCP2515.jpg)

As we have could connect and read a data, we could go further and connect to the car, read CAN bus with the CANable and 
CAN-viewer software

As we well know (or maybe some new people not yet) information among vehicle modules is exchanging via CAN bus messages.
Similarly to our network, but instead of PC as users, there are some amount of microcontrollers and modules. But to catch 
messages, its only 1st and small step. We have to encrypt it and decode in understandable for human eye view with reverse 
engineering approach as long as this information, which CAN bus messages belong to modules, is a sicret. 

You have to read a half of relevant internet sources and books. 
I can recommend to start from here: https://www.carhackingvillage.com/getting-started.

And highly recommend this book
![](CANhaking.png)

A lot of information about how do automotive network is designed and works.

As long as I study Python and its GUI Kivy, I have used it to design main App and deploy it on Raspberry platform. 
In the end I have got the App with 3 screens, which we can shift calling popup dialog window
1. Clasic view:

![](1screen.png)

2. With a little bit sport features:

![](2screen.png)

3. Service window with relevant sensors' data:

![](3screen.png)

Basically it works pretty well. 
Before CAN bus I had tried to read off data via OBDII interface with Python OBD library. It works, but my possibilities 
were limited with accessible PIDs. Only 7 data types 
with CAN bus we can get much more, the most difficult part is to encrypt messages and extract desirable information from 
there.

The retrieved CAN bus data App processes and send data to web server.
PHP scripts manages data inserting it from GSM module into database, extracts from DB and builds correspondant plots
with JS scripts.

http://vehicledata.atwebpages.com/index.html

Finally, we can observe our vehicle information on the plots, especially it's consumption and emition of CO2, GPS tracking



![](web1.png)![](web2.png)![](web3.png)


Trobleshooting which I was encountering with:
1. KIvy GUI is not the best framework for developing of Digital clusters. It works, but initially I preferred to add map
    as one of the screen widget, but App could not coupe with it, it significantly was loosing speed af CAN data processing
2. Power supply of RPI4 and A9G, Neo6m. If Raspberry Pi needs strict 5v current and takes 0.6A during loading OS it can impact
    our additional components if all of them are supplied with that same source. A6G and Neo6m demands 0.25A 5v current and if
    it changes a little bit during RPI4 load, it loses signal and can't connect with network or satellites.
3. Difference between Linux and Windows. Python is that same, but Linux has much wider variety of libraries. For CAN bus 
    exists good enough official library python-can and not published library from Peek-System company PCANBasic which we have 
    to assemble on our owns. This last works perfect for me and did not have troubles as other one which might rise up an 
    error: CAN bus was read to late with refer to cannotifier.py and its timeout
4. different pixel grid on laptop and rpi4 screen
5. Connect A9G, Neo6m to rpi4 and make it work together via UART 
