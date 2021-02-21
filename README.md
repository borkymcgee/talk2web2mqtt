# talk2web2mqtt
A small http server to turn http get requests from the talk2web pebble watch app into mqtt messages.

requires mosquitto_pub

# usage:
  put this in the url field of talk2web in the pebble app, replacing "YOUR_IP" with the ip you'll be running the server on
    "http://YOUR_IP/?text=" + text.replace("/ /g", "~")
