import json

file = open("formattedresults.json")
results = json.load(file)
file.close()

file = open("results.txt", "r")

while True:
    line1 = file.readline()
    if not line1:
        break
    line2 = file.readline()
    
    line1 = line1.split(";")
    line2 = line2.split(";")
    if line1[0] == "WIN":
        results["results"][line1[1]][line2[1]]["wins"] += 1
        results["results"][line1[1]]["win_util"].append(float(line1[2].strip()))
    else:
        results["results"][line1[1]][line2[1]]["losses"] += 1
        results["results"][line1[1]]["loss_util"].append(float(line1[2].strip()))
        
    if line2[0] == "WIN":
        results["results"][line2[1]][line1[1]]["wins"] += 1
        results["results"][line2[1]]["win_util"].append(float(line2[2].strip()))
    else:
        results["results"][line2[1]][line1[1]]["losses"] += 1
        results["results"][line2[1]]["loss_util"].append(float(line2[2].strip()))
    
    



file.close()















file = open("formattedresults.json", "w")
results = json.dumps(results, indent=4)
file.write(results)
file.close()


