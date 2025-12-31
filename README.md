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
```
set your password.

```bash
systemctl daemon-reload
systemctl enable ytadmin
systemctl start ytadmin
systemctl status ytadmin
journalctl -u ytadmin -f
```


## Usage
Open `http://localhost:9090`, login as admin. At "Manage targets" add items for monitoring (host, port, some name..).
