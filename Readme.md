# flask-pantilt-cam.py
A flask python3 live stream pan-tilt web page. Uses Keyboard or mouse buttons to control a pimoroni pantilthat assembly with 
attached pi camera module (Picamera2, Libcamera compatilble). 
Has Take Photo and View Photos onscreen buttons.

### Introduction

This program is a python3 flask web server application that allows control of a pimoroni pantilthat with a picamera2 compatible camera module attached.
A web page displays a live camera stream.
Keyboard arrow keys or on screen navigation buttons contol pantilt. A Take Photo button can be used to take, view and save an image to a specified folder.
The Save image folder path will be auto created per config.py setting.
A view photos button brings up a browse thumbnails image grid web page of peviously saved images. Click on Thumbnail to view full size image. 

I developed this app completely from scratch using only DeepSeek generative AI prompts for the coding. I did add the import from config.py feature myself,
plus misc edits and fixes. 

I called my DeepSeek AI assistant Codey. The basic version took approximately two hours for the AI interaction and testing on a Raspberry Pi 3B+. 
I started from scratch using just prompts and no example starting code. The Take and View photos feature took quite a bit longer due trouble shooting snd testing issues.

### Requirements

* Raspberry Pi computer (model 3 or greater) with Raspberry OS Bullseye or later (32 or 64 bit).
* Pimoroni pantilthat assembly  installed and working.
* A Pi Camera module (compatible with Picamera2, libcamera python libraries). Installed on pantilthat assembly and working.
* User should be comfortable with working in a terminal or SSH session
* User should have basic skills with computer hardware assembly, testing and problem solving issues.
* Internet access and local area network is required for installing software from Github.

### Installation

This was developed for a Raspberry Pi computer running Picamera2, Libcamera python library on , pimoroni or compatible pantilt hat assemby and a picamera2 compatible camera module.

Open a terminal or SSH session and clone the github repository.

    cd ~
    sudo apt update && sudo apt upgrade -y
    git clone https://github.com/pageauc/flask-pantilt-cam.git
    cd flask-pantilt-cam
    chmod +x flask-pantilt-cam.py
	
Edit the config.py settings	
	
	nano config.py
	
Edit the WEB_SERVER_PORT, WEB_SERVER_ROOT, WEB_PAGE_TITLE as required.
The WEB_SERVER_ROOT can be a relative or absolute path to the location of the images folder.
To exit and save nano changes Press Ctrl-x y  

To launch the web server

    ./flask-pantilt-cam.py
	
From a browser on your local network paste the flask url eg

    http://192.168.1.178:5010
	
![webserver browser screen shot](flask-pantilt-cam.png)
		

### Credits

Claude Pageau developed this application from scatch using DeepSeek AI.  
I called my assistant Codey. It was a rewarding and at times frustrating experience. I started from scratch using just prompts and no example starting code.

