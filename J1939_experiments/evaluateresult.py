import csv 
import os
import matplotlib.pyplot as plt
import sys

def sumresult(inputFile):

	''' Given a file name, returns the sum of the TP, TN, FP, FN scores of a 
	experiment_data result file'''

	tp = 0
	tn = 0
	fp = 0
	fn = 0
	tpr = []
	fpr = []
	val = []

	with open(inputFile, "r") as file:
		lines = file.readlines()

	for line in lines:
		#print(line)
		line_val = line.split()
		tn += int(line_val[0])
		tp += int(line_val[1])
		fn += int(line_val[2])
		fp += int(line_val[3])

		#calculate cummulative tpr and fpr for each point.
		tpr.append(tp/float(tp+fn))
		fpr.append(fp/float(fp+tn))



	val.append(tn)
	val.append(tp)
	val.append(fn)
	val.append(fp)

	return (val, tpr, fpr)



def main(rootdirectory):

	'''given a file directory, sums and returns all of the tn, tp, fn, fp for each file 
	contained in the directory. Stores the resulting output to a new folder experiment_summary'''

	directory = "roc_plots"   #output directory

	if not os.path.exists(rootdirectory+"/"+directory):
		os.makedirs(rootdirectory+"/"+directory)

	fileout = open(rootdirectory+'/summary_statistics.txt', 'w') 

	wr = csv.writer(fileout, delimiter='\t')


	for file in os.listdir(rootdirectory):
			#print(rootdirectory+"/"+file)
			if file.startswith("experiment_data"):
				#print(file)
				result, tpr, fpr = sumresult(rootdirectory+"/"+file)
				print(tpr)
				print(fpr)
				wr.writerow(result)
				plot_roc(tpr, fpr, sys.argv[1]+"/"+directory+'/roc_'+file+'.pdf')



	fileout.close()



def plot_roc(tpr, fpr, output):
 	print("Plotting ROC Curve ...")
 	color = "#008000"  # dark green
 	color1 = '#FF0000'
 	color2 = '#000000'

 	plt.figure(figsize=(5, 5), dpi=80)
 	plt.xlabel("False Positive Rate", fontsize=14)
 	plt.ylabel("True Positive Rate", fontsize=14)
 	plt.title("ROC Curve", fontsize=14)
 	plt.ylim([0, 1.5])
 	plt.xlim([0, 1.5])

 	plt.plot(fpr, tpr, color=color1, linewidth=1, label='0.40')
 	#plt.plot(fpr1, tpr1, linestyle='dashed', color=color2 ,linewidth=1, label='0.35')
 	plt.savefig(output)
 	#plt.show()







if __name__ == '__main__':
	if(len(sys.argv)!= 2):
		print("incomplete arguments. usage: evaluateresult.py experiment_result_root_directory")
		sys.exit(2)

	main(sys.argv[1])








