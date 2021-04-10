# oppo_bdp_103_CLI
This is a basic cli used to interface with the Oppo Blu Ray Player model 103

Heres the protocol document for interfacing with the oppo bdp device
https://drive.google.com/file/d/1DTB7EDHV9UHFX7biYdfWC_5PFvB-XtI6/view

# NOTE
This is not an optimized CLI. Im sure there are issues and to be frank, its just experimental code, but it helped me solve the problem at hand so I am uploading it.

# How to use
When you run the cli, it will listen for a UDP broadcast message containing the local IP and PORT to connect to the device on via TCP. Then after that happens you can just send the commands found in the protocol document.
