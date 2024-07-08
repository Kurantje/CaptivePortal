Basic configuration for RPI running BullsEye or Bookworm with NetworkManager temporarily enabling access point with captive portal:
1. Start web server
2. Enable access point with all traffic redirected to web server ip-adress:port
3. Connect to access point with other device (Apple, Android, ...) --> Device automatically opens browser showing form
4. Submit form with wifi credentials (ssid + password)
5. Stop the access point
5. Stop web server

Tested on Bookworm 32-bit en 64-bit, en BullsEye 32-bit en 64-bit
sh ./run.sh --> Activate the Captive Portal

Note: Port redirection (iptables) is not needed if the web server is hosted on port 80. However to do so you have to run the server as root, as ports 0-2024 are protected.
