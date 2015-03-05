import urllib
from bs4 import BeautifulSoup
import json 


#Function to get the list of .gam files directly under the given folder 

def get_gam_file_list(url) :
        try :
                htmltext = urllib.urlopen(url).read()
        except :
                print "Error occured while connecting to server. Please try again later!"
                exit()
        soup = BeautifulSoup(htmltext)

        items = soup.findAll('a')

        items = items[5:len(items)]

        files = []

        for item in items :
                text = item.text
                stext = str(text).split('.')
                #print stext

                if stext[len(stext)-1] == "gam" :
                        files.append(text)
                        
                

        return files



def get_segment(lines, i , n) :
        j = i+(n-1)*16
        end = j+16

        #print "===============================Segment "+str(n)+"================================="

        segment = ""

        while j<end :   

            spaces = ""

            m = (len(lines[j])-1)%12
            
            if m==0 :
                m=12

            while m<12  :
                spaces +=" "
                m+=1

            lines[j]+=spaces
            
            segment += lines[j][0:len(lines[j])-1] 
            #print lines[j].replace(" ",".")
            j=j+1

        return segment


def create_dictionary(segment1 , segment2) :
        
        split = [segment1[x:x+12] for x in range(0,len(segment1),12)]

        

        dict = {}

        for l in split :
            #print l
            dict[l[0]] = ["",""]
            
            dict[l[0]][0] = l[1:len(l)-1].lstrip().rstrip()


        split = [segment2[x:x+12] for x in range(0,len(segment2),12)]

        for l in split :
            #print l
            dict[l[0]][1] = l[1:len(l)-1].lstrip().rstrip()

        return dict


# Folder where you want to browse .gam files 
folder = "http://kurucz.harvard.edu/atoms/1401/"
#folder = "http://localhost/1401/"
files = get_gam_file_list(folder)

print "This a console based application to parse the first few lines of the selected .gam file , create a dictionary of it and output the result into corresponding JSON file in the ./jsons/ folder."

print "=================================================================================="
print "Given folder contains following .gam files please enter the index to continue. Any index other than given list of indices will result in the parsing of 'gf1401.gam' file."

i=1

for file in files :
        print str(i)+") "+file

        i+=1


index = raw_input()

print "=================================================================================="

try :
        index = int(index)
        if index>0 and index<8 :
                selected_file = files[index-1]
        else :
                selected_file="gf1401.gam"
except :
        selected_file= "gf1401.gam"

print "You selected " + selected_file

print "Downloading "+folder+selected_file


try :
        TEXT = urllib.urlopen(folder+selected_file).read()
except :
        print "Error occured while downloading. Exiting. Please try again!!"
        exit()


print "Parsing " + folder+selected_file

lines = TEXT.split('\n')

#Ignoring the first few lines :

i=0

while 1 :
    if lines[i][0]=='1' and lines[i+1][0] == '7' and lines[i+2][0]=='D' :
        break
    else :
        i+=1

segment1 = get_segment(lines,i,1)

segment2 = get_segment(lines,i,2)

dictionary = create_dictionary(segment1,segment2)

print "Creating JSON file with following data : \n"
print json.dumps(dictionary)+"\n"

output = open("./jsons/"+selected_file+".json",'w')

output.write(json.dumps(dictionary))

output.close()

print "Created ./jsons/"+selected_file+".json"

        

