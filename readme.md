
# Cloudflare ddns

- gets your own external / public IP via ifconfig.me
- get IP set on Cloudflare DNS for desired aRecord (i.e. office@example.com) via Cloudflare API interface
- if A record does not exist then create A record for office@example.com via Cloudflare API interface
- if A record exists but is changed, then update dns record for office@example.com via Cloudflare API interface

# Requirements:

- python3
- Cloudflare account with api key created
- dns zone on Cloudflare (like example.com)
- config.txt file set like this:
<code>
[cloudflare]
dns-zone=example.com
a-record=office.example.com
api-key=xxxxxxxxxxxxxxxxx
</code>

# How to use:
- cd to app_location

- create python environment
<code>python3 -m venv env</code>

- activate environment
<code>source env/bin/activate</code>

- install dependencies
<code>pip install -r requirements.txt</code>

- run application
<code>python3 cloudflare.py</code>

- cleanup
<code>deactivate</code>

