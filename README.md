Car Digital Cluster, Web dashboard with relevant information from CAN bus.


The working platform is Raspberry Pi 4

link: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/

![](rpi4.png)

communication with the CAN bus on the vehicle via CANable adapter.

![](CANable.png)

To send data via GSM I have been using A9GTkinter module:
link: https://docs.ai-thinker.com/gprs 

![](1.webp)

To read GPS data I have chosen well known and good recommended Neo6m GPS tracker:

![](neo6m.webp)

To debug our CAN module and verify its functionality was being used an Arduino Mega and MCP2515.

This setup can generate random CAN messages and send them to our CANable module.

![](ATMega2560+MCP2515_.png)


Python and its GUI framework Kivy as developing tool.
In the end was gotten app with 3 screens

1. Clasic view:

![](1screen.png)

2. With a little bit sport features:

![](2screen.png)

3. Service window with relevant sensors' data:

![](3screen.png)

We can call real time plotting touching a gauge and check hardware components taping following buttons

The retrieved CAN bus data is processed by the app and sent to a web server. PHP scripts manage the data by inserting it 
from the GSM module into a database, extracting it from the database, and building corresponding plots using JavaScript.

http://vehicledata.atwebpages.com/index.html

Finally, we can observe our vehicle's information through the plots, including details such as fuel consumption, 
CO2 emissions, and GPS tracking.

![](web1.png)![](web2.png)![](web3.png)

review on youtube:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/e2QAAOhgJqs/0.jpg)](https://www.youtube.com/watch?v=e2QAAOhgJqs)


