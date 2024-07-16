WiFiData.txt -> current format for the file that stores a message sent from the CDP portal

app.py -> Python script that operates the web server and locally hosting the CDP portal. It also handles writing the message contents to a file on the Pi. There are lines that can be commented out to either work on the Pi or a computer for testing.

index.html -> Mostly original html page from a previous iteration of the portal. Functionality is limited, and was mainly used as a placeholder.

jquery-3.5.1.min.js -> JQUERY functions used as a source file in the html code.

message.txt -> Local message file for testing the web interface on your own device. The real message.txt will go on the Pi, but having one to test is helpful.

new_index.html -> Up to date html page for the CDP portal.
