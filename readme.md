# DEV SETUP
Run: `docker compose -f docker-compose.dev.yml up --build -d`

## Frontend dev setup
Create a file Frontend/.env.local with these lines in it:
```
NEXTAUTH_SECRET=[secret key]
NEXTAUTH_URL=http://localhost:3000/

GATEWAY_URL=http://gateway:8081/
GATEWAY_URL_CLIENT=http://localhost:8081/
BACKEND_URL=http://backend:8000/
BACKEND_URL_NO_PORT_NO_HTTP=backend
GATEWAY_URL_NO_PORT_NO_HTTP=gateway
```
And to get secret key run this command in ubuntu: `openssl rand -base64 32`

## Connecting to PostgreSQL server
* On host go to `localhost:5420`
* Right click Servers, located on the left side of browser window, then select Register, server
* Fill in Name field with whatever name you like
* Go to Connection section
  * Host name/address: `host.docker.internal`
  * Port: `5432`
  * Maintenance database: `student`
  * Username: `student`
  * Password: `student`




# PRODUCTION SETUP
Make sure that ports are forwarded correctly and your domain name points to your server.
## HTTPS/TLS
### SETUP
1. create a file nginx/conf/default.conf.
2. Add this code, replace [domain-name] with your domain.
```
server {
    listen 80;
    listen [::]:80;
    server_name [domain-name] www.[domain-name];
    server_tokens off;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 [domain-name]$request_uri;
    }
}
```
3. Run `docker compose -f docker-compose.tls.yml up --build -d`.
4. Run `docker-compose -f docker-compose.tls.yml run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d [domain-name]`.
5. Provide email, read TOS and accept (y). After everything is done you should now have empty certbot/conf/live directory .
6. Add this code to default.conf, replace [domain-name] with your domain, replace [app-address-n] with yours app address, let's say 192.168.100.24:3000 .
```
server {
    listen 443 default_server ssl;
    listen [::]:443 ssl;
    server_name [domain-name];
    ssl_certificate /etc/nginx/ssl/live/[domain-name]/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/[domain-name]/privkey.pem;
    
    location / {
        proxy_pass [app-address-1]$request_uri;
    }
    location /api {
        proxy_pass [app-address-2]$request_uri;
    }
}
```
7. Run `docker-compose -f docker-compose.tls.yml restart`.
### RENEWAL
Run `docker-compose -f docker-compose.tls.yml run --rm certbot renew` every 3 months or earlier since certificates expire after this period of time.
#