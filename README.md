# twisted_proxy_https
Proxy for modifying https responses

# Install required packages
	pip install -r requirements.txt

# Run proxy
	twistd -y twisted.py 
## Point insights-client to connect to proxy
Add to insights-client.conf line:

	proxy=http://127.0.0.1:8000
Register insights-client:

	insights-client --register