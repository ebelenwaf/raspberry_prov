import babeltrace
import sys



# get the trace path from the first command line argument
trace_path = sys.argv[1]

trace_collection = babeltrace.TraceCollection()

trace_collection.add_trace(trace_path, 'ctf')
#Outputs the event keys of each trace that was recorded.
for event in trace_collection.events:
    print(', '.join(event.keys()))
