term = input("Enter term: ").upper()

with open(f"{term}/wl_percent.tsv", 'w') as f:
    with open(f"{term}/wl.csv", 'r') as g:
        next(g)
        f.write("course\tsection\tpercent\n")
        for line in g:
            line = line.split(',')
            course = line[0]
            section = line[1]
            off_waitlist = int(line[2])
            total = int(line[3])
            
            if total == 0:
                continue
            
            percent = off_waitlist / total
            f.write(f"{course}\t{section}\t{percent}\n")