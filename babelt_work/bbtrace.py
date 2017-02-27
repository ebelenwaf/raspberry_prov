import babeltrace
import sys



# get the trace path from the first command line argument
trace_path = sys.argv[1]

trace_collection = babeltrace.TraceCollection()

trace_collection.add_trace(trace_path, 'ctf')
#Outputs the event keys of each trace that was recorded.
results = open('output.txt', 'w')

for event in trace_collection.events:
    #print(', '.join(event.keys()))
    #results.write(', '.join(event.keys()))
    for key in event.keys():
        print(('%s : %s ,' %(key, event[key])))
        results.write(('%s : %s ,' %(key, event[key])))
    print('\n')
    results.write('\n')
