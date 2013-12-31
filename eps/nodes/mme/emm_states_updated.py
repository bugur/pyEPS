'''
Created on 16 Ara 2013

@author: Serkan
'''
from eps.utils.io import IoService
from eps.utils.statemachine import StateMachine
from eps.utils.config import Configuration
from eps.nodes.mme.states import Default
from eps.utils.statemachine import State

from ctypes.wintypes import BOOL

Attach = EPS_bearer_context = DETACH = network = UeInit = impDETACH = TAU = LLF = None


class EMMState(State):

    def __init__(self, context):
        super(EMMState, self).__init__()
        self.ioService = context["ioService"]
        self.config = context["config"]

class Deregistered(EMMState):

    def __init__(self, context):
        super(Deregistered, self).__init__(context)
    
    attachComplete = lambda sequenceNumber, esmMessage: (
        "nas",
        {
        },
        {
         "protocolDiscriminator": "EpsMobilityManagementMessage",
         "sequenceNumber": sequenceNumber,
         "messageType": "attachComplete",
         "securityHeaderType": "securityProtectedNasMessage",
         "esmMessageContainer": esmMessage
         }
    )
    
    activateDefaultEpsBearerContextAccept = \
        lambda epsBearerIdentity, procedureTransactionIdentity: (
        "nas",
        {
        },
        {
        "protocolDiscriminator": "EpsSessionManagementMessage",
        "epsBearerIdentity": epsBearerIdentity,
        "procedureTransactionIdentity": procedureTransactionIdentity,
        "messageType": "activateDefaultEpsBearerContextAccept",
        }                                                                                                                                                                                          
    )
    
    attachComplete = True                                      #Attach successful and default EPS bearer context is activated
    activateDefaultEpsBearerContextAccept = True
    
    def register(self):
        self.changeState(Registered)
    
    
        
class Registered(EMMState):

    def __init__(self, context):
        super(Registered, self).__init__(context)
    
    network =True 
    DETACH = True    
    UeInit = impDETACH = True
    TAU = False
    def register(self):
        self.changeState(Deregistered_Initiated)
        self.changeState(Deregistered)
        
class Deregistered_Initiated(EMMState):
    def __init__(self, context):
        super(Registered, self).__init__(context)
        
    DETACH = LLF = True 
    def register(self):
        self.changeState(Deregistered)   
        
        