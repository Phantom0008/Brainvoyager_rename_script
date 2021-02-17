import os, re, csv


global first_name, last_name, Code_Name

##Input Start##
root_data_path = _ # String path for the rot folder of your data
csv_file = _ # String path for the csv file 
first_name = _#column for the first name in your csv file (if you open it as excel...) 0 padded
last_name =  _#column for the last name in your csv file (if you open it as excel...) 0 padded
Code_Name = _ #column for the coded name in your csv file (if you open it as excel...) 0 padded
MP_String = _ #String folder in which the actual data is
folder_between= _  #String reoccuring pattern in the folder between the name folder and the data folder
len_coded_name = _ # int length of the coded names
exceptions = [] # string input here your exceptions such as ä,ü,ö etc in quotes example: ["ä","ü","á",...]
seperators = "[ _]" #seperates the folder name along these parameters example: [-]   Phantom0008-github-123-321 -> ["Phantom0008","github","123","321"]
##Input End##
rec = float(0)
unrec =float(0)

csv_file = open(csv_file, "r")
csv_file = csv.reader(csv_file, delimiter=";")
csv_file = [row for row in csv_file] #creates a generator list of your csv_file

for i in range(len(csv_file)): # repaces the exceptions specified in your exceptions with a "#" example: Müller -> M#ller 
	for j in exceptions:
		csv_file[i][first_name] = csv_file[i][first_name].replace(j, "#")
		csv_file[i][last_name] = csv_file[i][last_name].replace(j, "#")
	

def Brainvoyager_rename_anonymize(data_path, new_name): # Function for converting and anonymizing the DICOM files
	BrainVoyager.RenameDicomFilesInDirectory(data_path)
	BrainVoyager.AnonymizeDicomFilesInDirectory(data_path, new_name)
	
def Folderup(num_up, Path): #if calles go number of folders up in the folder hirachie
	x=Path
	for i in range(num_up):
		x=os.path.dirname(x)
	return x

def findName(folder_name):
	name = []
	global rec 
	global unrec
	folder_name = folder_name_o = re.split(seperators,folder_name) # splitting the folder along the specified parameters
	
	for i in range(len(folder_name)): #extracting the name of the folder -> get rid of all numbers
		if(folder_name[i].isdigit() != True):
				name.append(folder_name[i].lower()+" ")
	
	for i in range(len(name)): #Replace the folder name with the exceptions 
		for j in exceptions:
			name[i] = name[i].replace(j, "#")

	#name=name[:2]
	name_fol = "".join(name)
	name_fol = name_fol.strip()
	name_fol = name_fol.replace(" ", "_")
	name_fol = name_fol.strip("#")
	name_fol = name_fol.lower()

	for i in range(len(csv_file)): #Find the name in the csv file and returns the coded name
		first_name = re.compile(csv_file[i][first_name],re.IGNORECASE)
		last_name =  re.compile(csv_file[i][last_name],re.IGNORECASE)
		first_name_found = re.search(first_name,name_fol)
		last_name_found = re.search(last_name,name_fol)
		if (first_name_found != None and last_name_found != None):
			if (csv_file[i][first_name] != "" or csv_file[i][last_name] != ""):
				c_name = csv_file[i][Code_Name]
				rec += 1
				return c_name
	unrec +=1
	c_name = raw_input("%s not found please type name in: " %(folder_name_o)) #if name not found you can type the name in manually
	return c_name.rstrip("\r")
	

def Main(root_folder):
	print("Start main function")
	name = "Placeholder"

	for path, _, _ in os.walk(root_folder, topdown=False): #walks over the root folder tree
		folder_path = path
		folder_name = os.path.basename(folder_path)
		#print(folder_name)

		#print("Curr. Path:", path)
		if(name in path):
			continue

		if(re.search(MP_String, folder_name)!= None): #searches the specified data folder 
			#print("MP_Range found...")
			path_d  = Folderup(1, path)
		else:
			continue
		
		pattern_folder_between = re.compile(folder_between, flags=re.IGNORECASE)
		if(pattern_folder_between.search(os.path.basename(path_d)) != None): #checks if there is the folder between or not 
			print("Go over %s dir..." %(folder_between))
			path_d2 = Folderup(2, path)
		else: 
			path_d2 = path_d

		print("Find Coded Name...")
		if(len(os.path.basename(path_d2))>len_coded_name): #skips the renamed folder
			c_name = findName(os.path.basename(path_d2))
		else:
			continue
		name_rem = os.path.basename(path_d2)
		name = name_rem

		if(c_name != "" or None): #if a coded name is found rename the name folder, convert and aonoymize the DICOM files...
			try:
				#rename the folder to the coded name
				c_name_c = str("\\"+c_name)
				os.rename(str(path_d2),Folderup(1,path_d2)+c_name_c)
			except:
				continue

			print("Convert DICON Files... ")
			Brainvoyager_rename_anonymize(folder_path, os.path.basename(path_d2))
			print("Finished with",c_name,"/",name,"move to next name...")
			continue

Main(root_data_path)

if(unrec == 0):
	accuracy = "Div 0 error!"
else:
	accuracy = rec/(rec+unrec)
print("Finished with the job! wit an acc of:",accuracy) #returns the accuracy of the automatic results 


