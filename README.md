
## AirPy - Python wrapper for the AirVPN API
#### FlightAware XML v3

A Pythonic way to read and display data from AirpVPN API (based on the JSON ouput)key.

You can request an API key at https://airvpn.org/client/

#### API Documentation
https://airvpn.org/faq/api/

##### API calls
https://airvpn.org/api/?format=json&key=<your_api_key>&service=userinfo
https://airvpn.org/api/?format=json&key=<your_api_key>&service=status

#### Define an instance of AirPy with your api key


```python
from AirPy import Airvpn
APIKEY = "ebe97ae14821b0176c8066f62ee5c132e6b6ac034"
air = Airvpn(APIKEY,'nl')  # when you are located in the Netherlands
air = Airvpn(APIKEY,'gb')  # when you are located in the UK, and so on
```


```python
print air.user.connected
```

    True



```python
print air.connection
```

    Tarazed, 2018-12-01 15:59:18 UTC



```python
servers = air.servers()
for server in servers:
    print server
```

    Alathfar ,Maidenhead, gb, 185.103.96.132, 60, 83
    Algedi ,London, gb, 80.84.49.4, 39, 88
    Alshain ,London, gb, 217.151.98.162, 18, 80
    Asterion ,London, gb, 217.151.98.167, 33, 85
    Asterope ,Manchester, gb, 89.249.74.212, 22, 85
    Bellatrix ,London, gb, 88.150.240.7, 39, 79
    Betelgeuse ,Maidenhead, gb, 185.103.96.134, 45, 72
    Carinae ,Maidenhead, gb, 94.229.74.90, 35, 86
    Chow ,Manchester, gb, 89.249.74.217, 29, 80
    Dabih ,Manchester, gb, 82.145.37.202, 18, 72
    Denebola ,Maidenhead, gb, 185.103.96.133, 28, 81
    Kitel ,Maidenhead, gb, 185.103.96.131, 8, 102
    Minkar ,Maidenhead, gb, 185.103.96.130, 18, 102
    Naos ,Manchester, gb, 84.39.117.56, 25, 91
    Nashira ,Manchester, gb, 84.39.116.179, 11, 83
    Nunki ,Manchester, gb, 212.38.167.122, 0, 0



```python
print server.bw_max
```

    1000



```python
print server.location
```

    Manchester



