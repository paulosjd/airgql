"""
From a text file formatted as follows:
'Armagh Roadside' <circle cx="196.17" cy="618.2" r="3" fill="white" id="ARM6" />
'Belfast Centre' <circle cx="232.17" cy="596.58" r="3" fill="white" id="BEL2" />

Output to a new text file is:
<circle cx="196.17" cy="618.2" r="2" fill="white" id="ARM6" class="site-mark"/>
<text x="196.17" y="618.2" class="site-label" >Armagh Roadside</text>
<circle cx="232.17" cy="596.58" r="2" fill="white" id="BEL2" class="site-mark"/>
<text x="232.17" y="596.58" class="site-label" >Belfast Centre</text>
"""

with open('labels.txt') as f:
    circle_elems = f.readlines()

output = []
text_elems = []
for line in circle_elems:
    if 'circle' not in line:
        continue

    x = line[line.find('cx="') + 1:].split()[0]
    y = line[line.find('cy="') + 1:].split()[0]
    elem_id = line[line.find('id="'):].split()[0]
    elem_id = elem_id[:-1] + '_label' + '"'
    label = line.split('<cir')[0].replace('\"', '').replace('\'', '').strip()

    elem = f'<text {x} {y} class="site-label" {elem_id}>{label}</text>\n'
    line = '<' + line[line.find('circle'):]
    if 'class="site-mark"' not in line:
        line = '{}{}{}'.format(
            line[:line.find('/>')], 'class="site-mark"', line[line.find('/>'):])

    text_elems.append(elem)
    output.append(line)

output += text_elems

with open('label_out.txt', 'w') as f:
    f.writelines(output)
