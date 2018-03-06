import babeltrace
from babeltrace import CTFWriter
import sys
from collections import Counter
from collections import deque

def get_pruned_data(file_path, capacity):
    
    my_deque = deque(maxlen = capacity)
    trace_collection = babeltrace.TraceCollection()
    
    if trace_collection.add_trace(file_path,'ctf') is None:
        raise RuntimeError('Cannot add trace')
    
    for event in trace_collection.events:
        temp_dict = {}
        for key in event:
            temp_dict[key] = event[key]
        temp_dict['event_name'] = event.name
        if(len(my_deque) >= capacity):
            my_deque.popleft()
        my_deque.append(temp_dict)
    return my_deque

def create_stream_file(streamfile_dest, my_deque):
    
    writer = CTFWriter.Writer(streamfile_dest)
    clock = CTFWriter.Clock("A_clock")
    clock.description = "Simple clock"
    writer.add_clock(clock)
    
    writer.add_environment_field("Python_version", str(sys.version_info))
    stream_class = CTFWriter.StreamClass("test_stream")
    stream_class.clock = clock
    
    event_class = CTFWriter.EventClass("SimpleEvent")
    
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
    
    for item in my_deque:
        event = CTFWriter.Event(event_class)
        clock.time = item["timestamp"]
        integer_field = event.payload("value")
        integer_field.value = item["value"]
        integer_field = event.payload("event_id_count")
        integer_field.value = item["event_id_counter"]
        stream.append_event(event)
    stream.flush()

def main():
    capacity = 8
    file_path1 = 'ctf' #replace 'ctf' with a file path that has your stream file
    my_deque = get_pruned_data(file_path1, capacity)
    create_stream_file("new_file3", my_deque)
    print('{}'.format(my_deque))

if __name__ == '__main__':
    main()
