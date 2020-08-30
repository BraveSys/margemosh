import json

def convert_it(origin,destination):
    origin=open(origin,"r",encoding="UTF-8").read()
    parts=origin.split("#")
    print(parts)
    refined=[]
    for part in parts:
        part=part.split("\n")
        print("#",part)
        while("" in part):part.remove("")
        n=len(part)
        print(part)
        refined+=[[part[0],part[1:n-1],part[n-1]]]
    dest=open(destination,"w",encoding="UTF-8")
    dest.write(json.dumps(refined))
    dest.close()
    return refined

print("saved:",convert_it("raw.txt","dest.txt"))

test=open("dest.txt",encoding="UTF-8")
qs=json.loads(test.read())
print("loaded:",qs)
