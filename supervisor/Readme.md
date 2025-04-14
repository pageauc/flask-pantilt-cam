## flask-pantilt-cam.sh
The bash script manages supervisorctl background service for flask-pantilt-cam.py
per the associated [configuration .conf files ](https://raw.githubusercontent.com/pageauc/flask-pantilt-cam/refs/heads/main/source/supervisor/flask-pantilt-cam.conf) 
located in the supervisor folder. 
The scripts can start the .py scripts as background tasks under the specified user= in the conf file settings. 
These .conf files will by default not autostart run on boot but will attempt a restart if there is a program issue. 
Eg problem with camera.

The shell script install option creates a symlink at ***/etc/supervisor/conf.d*** folder back 
to the flask-pantilt-cam/supervisor folder .conf file.  Use ./flask-pantilt-cam.sh to manage options.
  
Note: Start on boot defaults to false, but can be enabled by editing the .conf file

For more details run 
    
    ./flask-pantilt-cam.sh help

example .    
./flask-pantilt-cam.sh help

    Usage: ./flask-pantilt-cam.sh [Option]

      Options:
      start        Start supervisor service
      stop         Stop supervisor service
      restart      restart supervisor service
      status       Status of supervisor service
      edit         nano edit /home/pi/flask-pantilt-cam/supervisor
      log          tail -n 200 /var/log/flask-pantilt-cam.log
      install      Install symbolic link for flask-pantilt-cam supervisor service
      uninstall    Uninstall symbolic link for flask-pantilt-cam supervisor service
      help        

    Example:  ./flask-pantilt-cam.sh status

    Wait ...

    flask-pantilt-cam                      RUNNING   pid 21464, uptime 3:45:51
    Done

Note:

The supervisor folder .conf file defaults to user=pi. The .sh scripts will modify the appropriate .conf file
per the logged in user (using sed).



    