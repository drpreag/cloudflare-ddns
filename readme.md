
# Cloudflare ddns

- gets your own external / public IP via ifconfig.me
- get IP set on Cloudflare DNS for desired aRecord (i.e. office@example.com) via Cloudflare API interface
- if A record does not exist then create A record for office@example.com via Cloudflare API interface
- if A record exists but is changed, then update dns record for office@example.com via Cloudflare API interface

# Requirements:

- python3
- Cloudflare account with api key created
- dns zone on Cloudflare (like example.com)
- config.txt section like this:
```
[cloudflare]
dns-zone=example.com
a-record=office.example.com
api-key=xxxxxxxxxxxxxxxxx
auth-email=<your cloudflare account email>
```

# How to use:
- cd to app_location

- create python environment
```
python3 -m venv env
```

- activate environment
```
source env/bin/activate
```

- install dependencies
```
pip install -r requirements.txt
```

- run application
```
python3 cloudflare.py
```

- cleanup
```
deactivate
```


# Hetzner firewall update

mandatory config.txt section:
```
[hetzner]
firewall-name=<firewall-name>
hcloud-token=<hetzner-api-token>
```