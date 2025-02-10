import json

with open("lab4\\sample-data.json", "r") as file:
    data = json.load(file)

interfaces = data.get("imdata")

for item in interfaces:
    attributes = item.get("l1PhysIf").get("attributes")
    dn = attributes.get("dn")
    description = attributes.get("descr")
    speed = attributes.get("speed", "inherit")
    mtu = attributes.get("mtu", "9150")

    print(f"{dn:<50} {description:<20} {speed:<7} {mtu:<6}")
