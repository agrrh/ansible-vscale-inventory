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
- `vscale_location_${LOCATION}` - hosts in `${LOCATION}` location
- `vscale_tag_${TAGNAME}` - hosts tagged as `${TAGNAME}`
