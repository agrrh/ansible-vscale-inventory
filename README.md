# Ansible dynamic inventory for Vscale

```
$ pip install -r requirements.txt

$ export VSCALE_API_TOKEN=changeme

$ ansible vscale -i inventory/vscale_inventory.py -u root -m ping
my-test-host | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
