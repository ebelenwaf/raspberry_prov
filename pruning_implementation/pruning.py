import babeltrace
from babeltrace import CTFWriter
import sys
from collections import Counter
import heapq
import itertools
from collections import deque

def get_pruned_data_FIFO(file_path, capacity):
    
    my_deque = deque(maxlen = capacity)
    counter = itertools.count() # To keep track of duplicates while sorting.
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
        event_copy = (temp_dict['priority'], next(counter), temp_dict)
        my_deque.append(event_copy)
    return my_deque


def get_pruned_data_priority(file_path, capacity):
    prio_queue = []
    counter = itertools.count() # To keep track of duplicates while sorting.
    trace_collection = babeltrace.TraceCollection()
    
    if trace_collection.add_trace(file_path,'ctf') is None:
        raise RuntimeError('Cannot add trace')
    
    for event in trace_collection.events:
        temp_dict = {}
        for key in event:
            temp_dict[key] = event[key]
        temp_dict['event_name'] = event.name
        event_copy = (temp_dict['priority'], next(counter), temp_dict)
        if len(prio_queue) >= capacity:
            heapq.heappushpop(prio_queue,event_copy)
        else:
            heapq.heappush(prio_queue, event_copy)
    return prio_queue

def create_stream_file(streamfile_dest, my_prio_queue):
    
    writer = CTFWriter.Writer(streamfile_dest)
    clock = CTFWriter.Clock("A_clock")
    clock.description = "Simple clock"
    writer.add_clock(clock)
    
    writer.add_environment_field("Python_version", str(sys.version_info))
    stream_class = CTFWriter.StreamClass("test_stream")
    stream_class.clock = clock
    
    event_class = CTFWriter.EventClass("canbus_rcv")
    
    # Controller_id
    string_field_controller_id = CTFWriter.StringFieldDeclaration()
    string_field_controller_id.encoding = babeltrace.CTFStringEncoding.UTF8
    event_class.add_field(string_field_controller_id, "controller_id")
    
    # Producer_id
    string_field_producer_id = CTFWriter.StringFieldDeclaration()
    string_field_producer_id.encoding = babeltrace.CTFStringEncoding.UTF8
    event_class.add_field(string_field_producer_id, "producer_id")
    
    # activity
    string_field_activity = CTFWriter.StringFieldDeclaration()
    string_field_activity.encoding = babeltrace.CTFStringEncoding.UTF8
    event_class.add_field(string_field_activity, "activity")
    
    # priority
    int32_type_priority = CTFWriter.IntegerFieldDeclaration(32)
    int32_type_priority.signed = False
    event_class.add_field(int32_type_priority, "priority")
    
    # ts
    int32_type_ts = CTFWriter.IntegerFieldDeclaration(32)
    int32_type_ts.signed = False
    event_class.add_field(int32_type_ts, "ts")
    
    # data0
    int8_type_data0 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data0.signed = False
    event_class.add_field(int8_type_data0, "data0")
    
    # data1
    int8_type_data1 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data1.signed = False
    event_class.add_field(int8_type_data1, "data1")
    
    # data2
    int8_type_data2 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data2.signed = False
    event_class.add_field(int8_type_data2, "data2")
    
    # data3
    int8_type_data3 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data3.signed = False
    event_class.add_field(int8_type_data3, "data3")
    
    # data4
    int8_type_data4 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data4.signed = False
    event_class.add_field(int8_type_data4, "data4")
    
    # data5
    int8_type_data5 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data5.signed = False
    event_class.add_field(int8_type_data5, "data5")
    
    # data6
    int8_type_data6 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data6.signed = False
    event_class.add_field(int8_type_data6, "data6")
    
    # data7
    int8_type_data7 = CTFWriter.IntegerFieldDeclaration(8)
    int8_type_data7.signed = False
    event_class.add_field(int8_type_data7, "data7")
    
    stream_class.add_event_class(event_class)
    stream = writer.create_stream(stream_class)
    
    for item in my_prio_queue:
        event = CTFWriter.Event(event_class)
        event.payload("controller_id").value = item[2]["controller_id"]
        event.payload("producer_id").value = item[2]["producer_id"]
        event.payload("activity").value = item[2]["activity"]
        event.payload("priority").value = item[2]["priority"]
        event.payload("ts").value = item[2]["ts"]
        event.payload("data0").value = item[2]["data0"]
        event.payload("data1").value = item[2]["data1"]
        event.payload("data2").value = item[2]["data2"]
        event.payload("data3").value = item[2]["data3"]
        event.payload("data4").value = item[2]["data4"]
        event.payload("data5").value = item[2]["data5"]
        event.payload("data6").value = item[2]["data6"]
        event.payload("data7").value = item[2]["data7"]
        stream.append_event(event)
    stream.flush()

def main():
    capacity = 1000
    file_path1 = 'ctf' #replace 'ctf' with a file path that has your stream file
    my_prio_queue = get_pruned_data_priority(file_path1, capacity)
    create_stream_file("new_file3", my_prio_queue) # replace 'new_file3' with a file destination
    print('{}'.format(my_prio_queue))

if __name__ == '__main__':
    main()
