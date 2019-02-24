with open('decided_20171229-0940.tsv') as f:
    lines = f.readlines()
    surf_list = []
    for line in lines[3:]:  # 最初にいらない三行がある
        line_list = line.rstrip().split('\t')
        if line_list[0] == 'EOS':
            print(''.join(surf_list).strip())
            surf_list = []
        elif len(line_list) >= 2:
            surf_list.append(line_list[1])
