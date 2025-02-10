import json

data = json.load(open("lab4\\sample-data.json", "r"))

interfaces = data.get("imdata")

for item in interfaces:
    attributes = item.get("l1PhysIf").get("attributes")
    dn = attributes.get("dn")
    description = attributes.get("descr")
    speed = attributes.get("speed", "inherit")
    mtu = attributes.get("mtu", "9150")

    print(f"{dn} {description} {speed} {mtu}")
