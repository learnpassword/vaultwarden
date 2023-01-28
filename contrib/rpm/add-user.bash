
sudo getent group vaultwarden >/dev/null  || sudo groupadd -r vaultwarden
sudo getent passwd vaultwarden >/dev/null || sudo useradd -r -g vaultwarden -d / -s /sbin/nologin vaultwardeno
