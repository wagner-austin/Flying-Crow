
# Dependencies for Flying Crow

This folder contains the necessary dependencies for installing `pygame` and related libraries for the Flying Crow project.

## Installation Instructions

To install the required dependencies manually, follow these steps:

1. Download and extract the `pygame` source:
   ```bash
   wget https://www.pygame.org/ftp/pygame-1.9.6.tar.gz
   tar -xzf pygame-1.9.6.tar.gz
   cd pygame-1.9.6
   ```

2. Install the dependencies:
   ```bash
   python3 setup.py -config -auto -sdl2
   python3 setup.py install cython
   ```

Alternatively, you can run the following one-liner to install everything:

```bash
pkg install sdl2 sdl2-image sdl2-ttf wget xorgproto && \
pip install cython && \
wget https://www.pygame.org/ftp/pygame-1.9.6.tar.gz && \
tar -xzf pygame-1.9.6.tar.gz && \
cd pygame-1.9.6 && \
python3 setup.py -config -auto -sdl2 && \
python3 setup.py install cython
```

## Notes

- This version of `pygame` does not include MIDI support (porttime).
