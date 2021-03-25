import numpy as np
import json

f  = open('/home/hoaileba/PythonFlask/NLP/MyProj/Api/config.txt')
# start_action = {}
list_action = []
list_start_action = []
string = ""
for line in f:
    l = line.strip()
    if (l != ''):
        list_action.append(l)
    else :
        list_start_action.append(list_action)
        list_action = []
# print(list_start_action)      
all_act  =[]
graph = {}
# print(len(list_start_action))
for act in list_start_action:
    id=  0
    w = act[id].split(' ')[-1]
    # print(w)
    all_act.append(w)
    for i in range(1,len(act)):
        intent = act[i].split(' ')[0]
        next_action = act[i].split(' ')[-1]
        if (next_action in all_act) == False:
            all_act.append(next_action)
            print(next_action)
        # print(intent, " -- ", next_action)
        graph[w+'/t'+intent] = next_action 
print(all_act)
for act in all_act:
    print(act,',')
# print(np.array(all_act))
# f = open('/home/hoaileba/PythonFlask/NLP/MyProj/DataGraph/graph_EVN_paycheck.json','w')
# # g = json.dumps(graph,indent = 6)
# json.dump(graph,f)
# # print(g)
# f.close()

