import csv, sys

def process(inputfile):
	writefile = open(inputfile.split(".")[0]+"_formatted.csv", 'wt')
	writekey = open(inputfile.split(".")[0]+"_metadata.csv", 'wt')
	keywriter = csv.writer(writekey)
	writer = csv.writer(writefile)

	columns = ["participant", "intro_salary", "intro_capable", "intro_efficient", "intro_skilled", "intro_intelligent", "intro_independent", "intro_motivated", "intro_committed", "intro_knowconsultants", "capable", "efficient", "skilled", "intelligent", "independent", "confident", "aggressive", "organized", "motivated", "committed_relative_others", "pros_cons", "exam_percentile", "late_days", "salary", "likelihood_promoted", "training_rec", "hire_rec", "manipulation", "candidate_name", "participant_sex", "participant_parent"]
	writer.writerow(columns)
	keywriter.writerow(columns)

	with open(inputfile, 'r') as data:
		reader = csv.reader(data, delimiter=',', quotechar='"')
		headers = next(reader)
		#### add a row with exact question wording
		header_explanations = []
		header_explanations.append("user id (from randomly generated code)")
		header_wording = next(reader)
		for i in range(16, 25):
			header_explanations.append(header_wording[i])
		for i in range(25, 42):
			header_explanations.append(header_wording[i])
		header_explanations.append("resume belongs to parent or nonparent")
		header_explanations.append("the name of the specific resume (since counterbalanced)")
		keywriter.writerow(header_explanations)
		
		#### having set up the file, go through the actual data
		next(reader) #skip headers
		total = 0
		for row in reader:
			row = [7 if item == "Extremely" else item for item in row] #correct all 7s
			row = [1 if item == "Not at all" else item for item in row] #correct all 1s
			row = [1 if item == "Most certainly will NOT be promoted" else item for item in row] #correct all promotable judgements
			row = [2 if item == "Moderately not promotable" else item for item in row] 
			row = [3 if item == "Moderately promotable" else item for item in row] 
			row = [4 if item == "Most certainly will be promoted" else item for item in row] 
			row = [1 if item == "Yes" else item for item in row] #correct yes/no answers
			row = [0 if item == "No" else item for item in row] 

			#### add all preliminary question answers
			first = []
			second = []
			userid = row[headers.index("mTurkCode")]
			first.append(userid)
			second.append(userid)
			for i in range(16, 25): #preliminary question answers
				first.append(row[i])
				second.append(row[i])

			#### switch on condition
			if row[headers.index("Finished")] == "True" and row[25] is not "": # condition 1, AllisonNon+SarahParent
				total += 1
				#### add first candidate answers
				for i in range(25, 42):
					first.append(row[i])
				first.append("nonparent")
				first.append("allison")
				#### add second candidate answers
				for i in range(42, 59):
					second.append(row[i])
				second.append("parent")
				second.append("sarah")

				first.append(row[headers.index("D1")])
				second.append(row[headers.index("D1")])
				if(row[headers.index("D4")] == "I am  a parent or legal guardian"):
					first.append(1)
					second.append(1)
				elif (row[headers.index("D4")] != ""):
					first.append(0)
					second.append(0)

				writer.writerow(first)
				writer.writerow(second)
			elif row[headers.index("Finished")] == "True" and row[59] is not "":# condition 2, AllisonParent+SarahNon
				total += 1
				for i in range(59, 76):
					first.append(row[i])
				first.append("parent")
				first.append("allison")
				for i in range(76, 93):
					second.append(row[i])
				second.append("nonparent")
				second.append("sarah")

				first.append(row[headers.index("D1")])
				second.append(row[headers.index("D1")])
				if(row[headers.index("D4")] == "I am  a parent or legal guardian"):
					first.append(1)
					second.append(1)
				elif (row[headers.index("D4")] != ""):
					first.append(0)
					second.append(0)

				writer.writerow(first)
				writer.writerow(second)
			elif row[headers.index("Finished")] == "False":
				print "Not Finished"
			else:
				print "ERROR:"
				print row
				print "\n"
				
			#### write data to csv
		#### close up when done 
		print "Processed " + str(total) + " complete participants."
		writefile.close()
		writekey.close()


def main():
	if len(sys.argv) < 2:
		print "usage: python analyze_qualtrics.py input_file.csv"
	else:
		process(sys.argv[1])

if __name__ == "__main__":
    main()