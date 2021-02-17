# Brainvoyager_rename_script
A programm for converting and anonymizing huge amouts of MRT fies via Brainvoyager

###Important###

I am not responsible for any damage of any kind!

If you use parts of it or the whole script please link me if it has helped you ;)

###Important###

Problem:

If you have many MRT data that you want to have renamed/anonymized and converted to a uniform data format via Brain Voyager this is a little program that could help you!
It has the focus on only renaming/anonymizing the patients/clients names for further processing of the data with the lack of privacy (ex. external analyzing software/companies).

For the worklow please look in the script :)

Explaining of the code:

Brainrename func: a combined function of the internal Brain Voyager Commands to rename and anonymize the patients names

Folderup func: a simple function to go up a specified number of folders up in the folder tree.

FindName func: 
This function opens the .csv file and iterates over it to make a simple list of first, last and coded names.
Then it compares the folder_name parameter with each of the list entries.
If it found the name pair it returns the coded name of the patient specified in the list.
It does this two times for the case the folder name has a "_" instead of a space in it.

Main func: The Main function walks via os.walk over the alte_Daten folder tree.
It finds the MP_range folder (specified by the MRT scanner the data is coming from) and the var folder (in case there is another folder between the name folder and the MP_range folder). Then it executes the FindName func and with the result it executes the Brainrename func.

The script completely walks over the tree and renames and anonymizes all names of your patients/clients for further processing.

I am very happy if you leave me some ritique/questions or correct some errors of any kind or develop it further.

Thank you in advance,
Phantom0008
