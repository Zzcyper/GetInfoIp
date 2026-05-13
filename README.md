# Description of the IP Geolocation Lookup Application

**IP Geolocation Lookup** is a Python Flask web application that allows users to search for information about any valid IPv4 address. Unlike the older desktop version, this updated version runs in the browser and works on both PC and mobile devices.

The application uses a modern dark-themed interface where users can enter an IP address or choose to automatically look up their own public IP address. After submitting a lookup request, the Flask backend contacts the `ipinfo.io` API and returns useful geolocation and network information.

The application displays details such as:

- IP address
- City
- Region
- Country
- Postal code
- Coordinates
- Timezone
- Organization / ISP
- Hostname
- Google Maps location link

## How It Works

The project uses Flask to serve both the frontend page and the backend lookup API.

When the user enters an IP address and clicks the **Lookup** button, the browser sends a `POST` request to the `/api/lookup` route. The backend validates the IP address format before sending a request to `ipinfo.io`.

If the lookup is successful, the returned JSON data is displayed inside the web interface. If the IP address is invalid, the request times out, or the API fails, the application shows a clean error message instead of crashing.

## Main Features

- Flask-powered backend
- Responsive HTML, CSS, and JavaScript frontend
- Works on desktop and mobile
- Lookup any valid IPv4 address
- Option to use your own public IP address
- IP format validation
- Error handling for failed requests and timeouts
- Google Maps integration for coordinates
- Modern dark UI design

## Technologies Used

- Python
- Flask
- Requests
- HTML
- CSS
- JavaScript
- ipinfo.io API
