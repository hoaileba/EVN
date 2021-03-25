
import json
path_graph = '/MyProj/DataGraph/graph.json'

class Graph:
    def __init__(self,path_action):
        self.connection = {}
        self.action_text = {}
        self.checked_action = {}
        with open(path_action) as f:
            all_action = json.load(f)
        for action in all_action:
            self.checked_action[action] = 0

    def check_visited(self,action):
        return checked_action[action]
    
    def reset_checked(self):
        for action in self.checked_action:
            self.checked_action[action] = 0

    def check_intent(self,start_action,intent):
        if ((start_action,intent) in self.connection) == False :
            return False
        return True

    def get_next_action(self,start_action,intent):
        if ((start_action,intent) in self.connection) == False :
                return 'action_sorry'
        return self.connection[(start_action,intent)]


    def get_text_action(self,action):
        return self.action_text[action]

    def add_branch(self, start_action,target_action,intent):
        # key = sno/
        self.connection[(start_action,intent)] = target_action

    def save_graph(self,path):
        g = {}
        for p in self.connection:
            start_action,intent = p
            target_action = self.connection[p]
            key = start_action+'\t'+intent
            g[key] = target_action
        with open(path,'w') as f:
            json.dump(g,f)


    def load_Graph(self,path):
        with open(path,'r') as f:
            data = json.load(f)
        for id in data:
            start_action = id.split('\t')[0] 
            intent = id.split('\t')[1]
            target_action = data[id]
            self.connection[(start_action,intent)] = target_action

    def load_text(self,path):
        with open(path,'r') as f:
            data = json.load(f)
        for action in data:
            self.action_text[action] = data[action]
         




    