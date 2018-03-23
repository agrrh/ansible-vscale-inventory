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

Script generates following groups:

- `vscale` - all available hosts
- `vscale_location_${LOC}` - hosts in `${LOC}` location, e.g. `vscale_location_spb0`
- `vscale_tag_${TAG}` - hosts tagged as `${TAG}`, e.g. `vscale_tag_frontend`
