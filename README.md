hi this is a project i did over winter break in 2018. its a digital dashboard of my car that displays RPM, speed, fuel level, and coolant temperature. it gives an alert message for any diagnostic trouble codes (check engine light), so save yourself a trip to the mechanic. it also has a button that launches a rear-view camera.

![digital dashboard](https://raw.githubusercontent.com/isaiahkahler/digital-dashboard/master/media/pi.jpg "digital dashboard")

even though nobody will ever use this or attempt to make this but me, heres some ~documentation~ about how it works and remaking it:

### parts
- raspberry pi 3
- raspberry pi touchscreen
- USB OBD-II adapter
- EasyCap UTV007 USB video capture thing (find it on amazon)
- rear-view camera with composite output
- some USB ports in your car, for power

### hardware install

i got one of the backup cameras that installs behind the license plate, which i recommend. routed the cable through the back seats and up into the front dash.

![Reverse Camera](https://raw.githubusercontent.com/isaiahkahler/digital-dashboard/master/media/reverse1.jpg "Reverse Camera")
![Reverse Camera 2](https://raw.githubusercontent.com/isaiahkahler/digital-dashboard/master/media/reverse2.jpg "Reverse Camera 2")
![Camera Cable](https://raw.githubusercontent.com/isaiahkahler/digital-dashboard/master/media/wiring2.jpg "Camera Cable")

in order to power the camera, you have to wire it up to one of your reverse lights, which i just did by cutting the wires, soldering on, and then taped it up (probably not ideal, but it works).

![Reverse Wiring](https://raw.githubusercontent.com/isaiahkahler/digital-dashboard/master/media/wiring.jpg "Reverse Wiring")

the OBD-II thing is always plugged into my car's port. i didn't want to go with a bluetooth one because of like latency and battery drain and whatnot,but the software should work either way.

![OBD-II Adapter](https://raw.githubusercontent.com/isaiahkahler/digital-dashboard/master/media/obd.jpg "OBD-II Adapter")

### software setup

download code! then
```
npm install
npm run build
```
if all of these dependencies are out of date by the time youre reading this, oh well! sorry!

easycap driver is built into raspbian now! so just 
`sudo apt-get -y install mplayer` for the viewer software.

you can test your camera if you want with
```
mplayer tv:// -tv driver=v4l2:norm=NTSC_443:device=/dev/video0 -framedrop
```

make a special fifo file! (idk what this actually is, but 'fifo' sounds funny to me. this file will give control over the player software from the python script )
```
mkfifo /home/pi/digital-dashboard/fifofile
```

some python packages are needed
```
pip3 install obd
pip3 install websockets
```

to make the code run at startup, edit the autorun file. this has changed over time with raspbian but right now in stretch do
```
sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
```
add to the end
```
@python3 /home/pi/digital-dashboard/server.py
```
you might have to install python3, so maybe do that

the `server.py` script does everything, so maybe a lot could go wrong. you'll probably need to change a few things around too.

on line 14, change the `connection` variable to use the standard OBD constructor. it'll auto connect to your OBD reader, and then your car.
```
connection = obd.OBD()
```

do some exploring and see what cool information you can get from your car. there's a [wikipedia page](https://en.wikipedia.org/wiki/OBD-II_PIDs) filled with all of the possible values your car can give and the [python docs](https://python-obd.readthedocs.io/en/latest/) for the library show you how to find out what your car supports. 

your car might not be able to get some info the dash requests (RPM, speed, coolant temp, and fuel level), while you may want to include some that the dash doesn't support, so go change stuff. 

actually, as of writing this, my car doesn't support the fuel level command, so it's commented out in all of the code. if you want to enable that, change `server.py` and `dash.tsx`.

okay im tired now, email me if you have a question isaiahwkahler@gmail.com