import babeltrace
from babeltrace import CTFWriter
import sys
import tempfile
from collections import Counter
from collections import deque


#############################################################################
#    Function to Prunn the data and put in a deque                          #
#    @param trace_path: The path to the stream file                #
#           capacity: The capacity of the deque                             #
############################################################################

def getPrunnedData(trace_path, capacity):
    
    myDeque = deque(maxlen = capacity)
    trace_collection = babeltrace.TraceCollection()
    
    # Raise an exception
    if trace_collection.add_trace(trace_path,'ctf') is None:
        raise RuntimeError('Cannot add trace')
    
    # Gather all the information and discard what you dont easy.
    # print(trace_collection)
    for event in trace_collection.events:
        temp_dict = {}
        for key in event:
            temp_dict[key] = event[key]
        temp_dict['event_name'] = event.name
        if(len(myDeque) >= capacity):
            myDeque.popleft()
        myDeque.append(temp_dict)
    return myDeque
##########################################################################################
#    Function to Prunn the data and put in a deque                                       #
# @param streamFileDestination: The location of where you want the streamfile to go      #
#        myDeque: contains a collection of all the events in the stream file             #
##########################################################################################
def createStreamFile(streamFileDestination, myDeque):
    
    writer = CTFWriter.Writer(streamFileDestination)
    clock = CTFWriter.Clock("A_clock")
    clock.description = "Simple clock"
    writer.add_clock(clock)
    
    writer.add_environment_field("Python_version", str(sys.version_info))
    stream_class = CTFWriter.StreamClass("test_stream")
    stream_class.clock = clock
    
    event_class = CTFWriter.EventClass("SimpleEvent")
    
    # We can create multiple events here
    # Create a int32_t equivalent type
    int32_type = CTFWriter.IntegerFieldDeclaration(32)
    int32_type.signed = True
    event_class.add_field(int32_type, "value")
    
    # Create a int32_t equivalent type for the event_id_count
    int32_type = CTFWriter.IntegerFieldDeclaration(32)
    int32_type.signed = True
    event_class.add_field(int32_type, "event_id_count")
    
    
    stream_class.add_event_class(event_class)
    stream = writer.create_stream(stream_class)
    
    for item in myDeque:
        event = CTFWriter.Event(event_class)
        clock.time = item["timestamp"]
        integer_field = event.payload("value")
        integer_field.value = item["value"]
        integer_field = event.payload("event_id_count")
        integer_field.value = item["event_id_counter"]
        stream.append_event(event)
    
    stream.flush()

######################################################################################
# A function to test the code                                                        #
# Note: you can change the function createStreamFile("new_file3", my_deque)          #
# To accept only a stream path and then call the getPrunnedData inside the function  #
######################################################################################
#initialize variables
capacity = 8

# File path hard code
trace_path1 = 'ctf'
my_deque = getPrunnedData(trace_path1, capacity)
createStreamFile("new_file3", my_deque)
print('{}'.format(my_deque))

#######################################################################






