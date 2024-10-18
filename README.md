# Flying Crow

**Flying Crow** is a simple side-scrolling game built with Python and Pygame. Control a crow as it walks and flies through a scrolling background, with clickable buttons for game control.

## Features
- Crow walk and fly animations.
- Scrolling background and clouds.
- Start, pause, resume, and restart buttons.

## How to Play
1. **Jump**: Click anywhere to make the crow jump.
2. **Pause/Resume**: Use the buttons to pause or resume the game.
3. **Restart**: Restart the game or return to the main menu.

## How to Run
1. Install Pygame:
   ```bash
   pip install pygame
   ```
2. Run the game:
   ```bash
   python flying_crow_v1.py
   ```

Make sure the image assets are in the `assets` folder for the game to function correctly


# VNC Setup for Termux with bVNC Viewer

This guide walks through the steps to set up a VNC server on Termux and connect to it using the **bVNC Free** app for Android. This allows you to run and view graphical applications from Termux.

## Steps to Set Up VNC with Termux

### 1. Install Necessary Packages in Termux
Install the `x11-repo`, a VNC server, and a lightweight window manager (Openbox):
```bash
pkg install x11-repo
pkg install tigervnc xorg-server openbox
```

### 2. Start the VNC Server
Start the VNC server with a resolution of **3088x1440** to match fullscreen display:
```bash
vncserver :1 -geometry 3088x1440
```
This starts the VNC server on display `:1` with a resolution of 3088x1440. You will be prompted to set a password when starting the VNC server for the first time.

### 3. Set the `DISPLAY` Environment Variable
Ensure that the `DISPLAY` environment variable is correctly set for the VNC session:
```bash
export DISPLAY=:1
```

### 4. Run the Window Manager (Openbox)
Start Openbox to provide a lightweight graphical interface in the VNC session:
```bash
openbox-session &
```

### 5. Install the bVNC Viewer on Your Android Device
You used the **bVNC Free** app to connect to the VNC server. Download it from the Play Store:
[bVNC Free - Google Play](https://play.google.com/store/apps/details?id=com.iiordanov.freebVNC)

### 6. Set Up bVNC Viewer
- Open the bVNC app and configure the connection:
  - **VNC Server**: `localhost:5901`
  - **Password**: Use the password you set when starting the VNC server in Termux.
- Click **Connect** to establish the connection to the VNC session.

### 7. Test the Setup
To verify that the graphical environment is working, run a simple graphical application in Termux, such as `xterm`:
```bash
pkg install xterm
xterm &
```
This should open a terminal window in the VNC viewer.

### 8. Test with Pygame (Optional)
Once the VNC session is working, you can test running your Pygame script:
```bash
python flying_crow_v1.py
```
This will launch your Pygame window in the VNC viewer, allowing you to interact with it graphically.

---

## Summary of Actions
1. Installed VNC server, X11 repo, and Openbox in Termux.
2. Started the VNC server and set the `DISPLAY` environment variable.
3. Ran Openbox to provide a graphical interface.
4. Installed the **bVNC Free** app on Android to connect to the VNC server.
5. Verified the setup by running graphical applications like `xterm` and Pygame.
