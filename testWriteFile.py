# Open the file for reading
with open('code.py', 'r') as f:
    lines = f.readlines()  # read the lines into a list
    print(lines)

#Modify the list
lines.insert(2, "adding more words\n")  # insert new line between lines 2 and 3

# Open the file for writing
with open('code.py', 'w') as f:
    f.writelines(lines)  # write the modified lines back to the file
