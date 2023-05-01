import json

# Load current results into dict
file = open("formattedresults.json")
results = json.load(file)
file.close()

# Read unformatted results

file = open("results.txt", "r")

while True:
    # read two lines as each battle writes two lines
    line1 = file.readline()
    # stopping condition for loop
    if not line1:
        break
    line2 = file.readline()
    
    # separate result line into list
    line1 = line1.split(";")
    line2 = line2.split(";")
    
    # determine if first line is for the win
    # and credit the agent type with a win or loss and the utility
    if line1[0] == "WIN":
        results["results"][line1[1]][line2[1]]["wins"] += 1
        results["results"][line1[1]]["win_util"].append(float(line1[2].strip()))
    else:
        results["results"][line1[1]][line2[1]]["losses"] += 1
        results["results"][line1[1]]["loss_util"].append(float(line1[2].strip()))
        
    # determine if first line is for the win
    # and credit the agent type with a win or loss and the utility
    if line2[0] == "WIN":
        results["results"][line2[1]][line1[1]]["wins"] += 1
        results["results"][line2[1]]["win_util"].append(float(line2[2].strip()))
    else:
        results["results"][line2[1]][line1[1]]["losses"] += 1
        results["results"][line2[1]]["loss_util"].append(float(line2[2].strip()))
    
file.close()

# Write new results to file
file = open("formattedresults.json", "w")
results = json.dumps(results, indent=4)
file.write(results)
file.close()