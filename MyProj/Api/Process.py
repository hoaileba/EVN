from .Model_Intent import Model_Cls
from .Model_NER import Model_NER
from .Graph import Graph
from .Access_database import Database
import json
from datetime import datetime
from random import randint

PATH_GRAPH = 'MyProj/DataGraph/graph_EVN_loss_power.json'
PATH_INTENT = 'MyProj/weight_model/weight.h5'
PATH_TEXT = 'MyProj/DataGraph/text_action _EVN_loss_power.json'
THRESHOLD = 0.85

database = Database()

model_intent = Model_Cls()
model_intent.create_model()
model_intent.load_weight(PATH_INTENT)

model_ner = Model_NER()
model_ner.create_model_test()

graph = Graph()
graph.load_Graph(PATH_GRAPH)
graph.load_text(PATH_TEXT)


class Process_Case:
        def __init__(self,db,graph):
                self.db = db
                self.graph = graph
                # pass
        def process_by_score(self,intent,score):
                if score < THRESHOLD:
                        # intent = 'fallback'
                        return 'fallback'
                return intent
        
        def check_exist_path(self,previous_action, intent):
                if self.graph.check_intent(previous_action,intent) == False:
                        # intent = 'fallback'
                        return 'fallback'
                return intent
        
        def check_entities(self,intent,entites):
                if intent == "intent_provide_name" and entites == [{}]:
                        return "fallback"
                if intent == "intent_provide_address" and entites == [{}]:
                        return "fallback"
                if intent == 'provide_address' and entites == [{}]:
                        return 'fallback'
                if intent == 'provide_name' and entites == [{}]:
                        return 'fallback'
                if intent == 'provide_number_phone' and entities == [{}]:
                        return 'fallback'
                if intent == 'provide_code_customer' and entities == [{}]:
                        return 'fallback'
                return intent
        
        def check_fallback_2nd(self,intent,previous_intent):
                if previous_intent == intent and (intent =='fallback' or intent == 'cant_hear') == True:
                        intent = intent+'_1'
                else :  
                        intent = intent
                return intent
        def check_visited_(self,previous_action,action, intent):
                if self.graph.check_visited(action) >=1 and( previous_action == 'action_ask_search_method' or previous_action == 'action_ask_method' ):
                        return 'fallback'
                return intent
                
        def check_num_in_repbranch(self, ):
                pass

        def 


        def check_exist_database(self,action,entites,):

                if action == 'action_check_power':
                        result = self.db.check_lich(entities)
                        if result == 0:
                                final_intent = 'check_no'
                        else :
                                final_intent = 'check_yes'
                        # final_action = (self.graph.get_next_action(action,final_intent))

                if action == 'action_check_name':
                        result = self.db.check_lich(entities)
                        if result == 0:
                                final_intent = 'check_no'
                        else :
                                final_intent = 'check_yes'
                        # final_action = (self.graph.get_next_action(action,final_intent))
                        



class Process:
        def __init__(self,model_intent, model_ner,graph, db):
                self.model_intent = model_intent
                self.model_ner = model_ner
                self.graph = graph
                self.db = db
                
        def get_pred_intent(self,text):
                return self.model_intent.get_predict(text)
        
        def get_pred_entities(self,text):
                return self.model_ner.get_predict_test(text)
        
        def regex_phone(self, number):
                pass

        def regex_code(self,number):
                pass

        def create_init(self):
                now = datetime.now()
                
                # print("now =", now)
                ra = randint(0,100000)
                dt_string = now.strftime("%d/%m/%Y/%H/%M/%S")+str(ra)
                text =  (self.graph.get_next_action('action_Start','begin'))
                text = self.graph.get_text_action(text)
                print(text)
                data = {
                        'sender':dt_string,
                        'action': 'action_ask_distric_name',
                        'intent' : 'begin' ,
                        'text' : "",
                        'entities': ""
                }
                self.db.write_Convers(data)
                self.db.write_Message(data)
                return {
                        "text":text,
                        'sender':dt_string
                }
                
        def create_respone(self,request):
                
                text = request['message']
                sender = request['sender']

# get raw predict intent, score and entities
                intent, score  = self.get_pred_intent(text)
                entities = self.get_pred_entities(text)
                print('raw_predict_intent: ', intent,' - score: ',score)
                print('raw_predict_entities: ', entities)

# get last action 
                previous_request = self.db.get_last_request(sender)
                previous_action = previous_request['action']
                previous_intent = previous_request['intent']
# handle fallback by score -------------- filter 1
                if score < THRESHOLD:
                        intent = 'fallback'

        

               
                
#check exist intent  ---------------- filter 2
                if self.graph.check_intent(previous_action,intent) == False:
                        intent = 'fallback'
                
                final_intent = intent

# check 2nd fallback ---------------- filter 3
                if intent == 'intent_provide_name' and entities == [{}]:
                        intent = 'fallback'

                if action == 'action_check_name':
                        result = self.db.check_lich(entities)
                        if result == 0:
                                final_intent = 'check_no'
                        else :
                                final_intent = 'check_yes'
                        final_action = (self.graph.get_next_action(action,final_intent))

                # if action ==

                current_action = (self.graph.get_next_action(previous_action,final_intent))
                final_action = current_action

#check entities  ------------------- filter 4
                
                
                
                if previous_intent == intent and (intent =='fallback' or intent == 'intent_cant_hear') == True:
                        intent = intent+'_1'
                else :  
                        intent = intent

# check name and address exists in database or not
                if action == 'action_check_power':
                        result = self.db.check_lich(entities)
                        if result == 0:
                                final_intent = 'check_no'
                        else :
                                final_intent = 'check_yes'
                        final_action = (self.graph.get_next_action(action,final_intent))

                if action == 'action_check_name':
                        result = self.db.check_lich(entities)
                        if result == 0:
                                final_intent = 'check_no'
                        else :
                                final_intent = 'check_yes'
                        final_action = (self.graph.get_next_action(action,final_intent))
                        
                if final_intent == 'intent_provide_name':
                        entities = [{'start':0,'end':10,'value': 'lê bá hoài'}]
                if  final_intent == 'intent_provide_address':
                        entities = [{'start':0,'end':9,'value': 'trung văn'}]
                
                
                text = self.graph.get_text_action(final_action)
                entities = str(entities)
                # print(entities)
                data = {
                        'sender':sender,
                        'action': final_action,
                        'intent' : final_intent ,
                        'text' : text,
                        'entities': entities
                }
                self.db.write_Message(data)
                print(data)
                return data


process = Process(model_intent,model_ner,graph,database)      