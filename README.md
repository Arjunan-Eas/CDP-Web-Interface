static -> JavaScript files used in the web portal. Located in this folder because Flask serves static files from a specific folder. (jquery-3.5.1.min.js and socket.io.min.js)

WiFiData.txt -> current format for the file that stores a message sent from the CDP portal

app.py -> Python script that operates the web server and locally hosting the CDP portal. It also handles writing the message contents to a file on the Pi. There are lines that can be commented out to either work on the Pi or a computer for testing.

index.html -> Up to date html page for the CDP portal.

legacy_CDP_portal.html -> Original CDP web interface with all original CDP functions. Superceded by index.html.

production_app.py -> Uncommented version. Use this for the Raspberry Pi.

received_message.txt -> Test file for messages received from network

sent_message.txt -> Test file for messages sent by client
