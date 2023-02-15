import json
import subprocess

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

data = {"public-subnet-list":[]}

publicsubnet = ["",""]
publicmask = ["24", "22"]

for i in range(len(publicsubnet)):
    data["public-subnet-list"].append({
                "ip-address":f"{publicsubnet[i]}",
                "mask-length":f"{publicmask[i]}",
                "private-subnet-list":
                [
                    {
                        "ip-address":"",
                        "mask-length":"24"
                    },
                ]
            })
x=json.dumps(data)
print(x)
