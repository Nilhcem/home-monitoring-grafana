## Install dependencies

```sh
sudo pip install -r requirements.txt
```

Run:

```sh
./main.py
```

## Install bluepy on Raspberry:

```sh
$ sudo apt-get install python-pip libglib2.0-dev
$ sudo pip3 install -r requirements.txt
$ ./main.py
```

Run when you boot into the LXDE environment

```sh
sudo nano ~/.config/lxsession/LXDE-pi/autostart
```

Add at the end of file:

```
@python3 /home/pi/mijia/main.py
```

Restart your Raspberry Pi into the LXDE environment.

