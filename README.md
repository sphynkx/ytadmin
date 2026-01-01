Admin panel for monitoring and manage of all [YurTube](https://github.com/sphynkx/yurtube) apps and services. Monitoring implemented by gRPC calls via an external utility.


## Install
```bash
dnf -y install grpcurl
cd /opt
git clone https://github.com/sphynkx/ytadmin
cd ytadmin
python3 -m venv .venv
install/pipinstall
cp install/ytadmin.service /etc/systemd/system/
```
Create `.env`:
```conf
ADMIN_USERNAME=admin
ADMIN_PASSWORD=SECRET

ADMIN_PULL_ENABLED=true
PUSH_STALE_THRESHOLD_SEC=60

# YurTube DB
DB_NAME=yt_db
DB_USER=yt_user
DB_PASS=SECRET
DB_HOST=192.168.7.3
DB_PORT=5432
```
set your passwords.

Go to YurTube side.  Edit `/var/lib/pgsql/data/pg_hba.conf` (or find placement of this file in your system), add line with IP of ytadmin side:
```conf
host    yt_db           yt_user   192.168.7.8/32   scram-sha-256
```
and restart postgres.

```bash
systemctl daemon-reload
systemctl enable ytadmin
systemctl start ytadmin
systemctl status ytadmin
journalctl -u ytadmin -f
```


## Usage
Open `http://localhost:9090`, login as admin. At "Manage targets" add items for monitoring (host, port, some name..).
