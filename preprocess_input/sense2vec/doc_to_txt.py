'''
import PyPDF2 as pyPdf

filename = "intro_to_envi.pdf";
pdf = pyPdf.PdfFileReader(open(filename, "rb"))
i = -1;
for page in pdf.pages:
    i = i + 1;
    print("---Page ", i, ":--------------------------------");
    print (page.extractText())
    
    input("Press Enter to continue...")
    
'''

import textract
import shutil
from cStringIO import StringIO
import os

######################
## Find all pdfs
#########################
source_root = "inputs";
done_root = "done";
output_root = "inputs";
doc_list = [];
i = -1;
for afile in os.listdir(source_root):
    if afile.endswith(".pdf") or afile.endswith(".epub"):
        i = i+1;
        doc_list.append(afile);
        #print(file)
#print (pdf_list);
#exit();


def convert_doc_to_txt(path):
    text = textract.process(path);
    return text

def move_doc_to_done(source_path, done_path):
    result = shutil.move(source_path, done_path);
    return result;
    
######################
## Convert all pdfs
#########################
print("\n");
print("Converting all docs...");
for file_name in doc_list:
    #file_name = "lonely_planet.pdf";
    source_path = source_root + "/" + file_name;
    done_path = done_root + "/" + file_name;
    print (" -- Converting " + source_path);
    text = convert_doc_to_txt(source_path);
    #print(text);

    f = open(output_root+"/"+file_name[0:-4]+'.text', 'w+')
    f.write(text);  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it

    #print ("   -- Moving it to " + done_path);
    #move_doc_to_done(source_path, done_path);

