#start each file with
"""
0, 0, Header, 1,1, 480
1, 0, Start_track
1, 0, Program_c, 0, 0
"""
#and end each file with
"""
1, 112094, End_track
0, 0, End_of_file
"""
#for note on note off lines:
"""
1st entry is always '1'
3rd entry is either 'Note_on_c' or 'Note_off_c'
4th entry is always '0'
6th entry is always 0 IF 3rd entry is 'Note_off_c'


output file will be at least the length of the 2nd entry of the 'End_track' line (in characters)
This number is the total units of time in the piece
For every unit of time that doesn't appear as a 2nd entry in a note on off line:
a space character will be written

#A constant velocity will be used (70 for example) ie all notes will be the same volume
88 characters will be used for each level of velocity (4 levels - 4x88 characters)

Notes (represented as numbers from 0-88 in the 5th entry) will be mapped to 89 ascii characters

Notes that start on the same time unit will appear together ( :DhS )

The first time a note is seen it is equivalent to note_on
The second time it is equivalent to note_off
This should encode different note lengths
"""
import csv
from collections import Counter

velocity = 0
setUsed = None
fileOut = []
minNote = 23

piano = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0","!",'"',"£","$","€","%","^","&","*","(",")","-","_","+","=","`","¬","¦",";",":","'","@","#","~",",","."]
mezzoforte = ["ß","à","á","â","ã","ä","å","æ","ç","è","é","ê","ë","ì","í","î","ï","ð","ñ","ò","ó","ô","õ","ö","ø","ù","À","Á","Â","Ã","Ä","Å","Æ","Ç","È","É","Ê","Ë","Ì","Í","Î","Ï","Ð","Ñ","Ò","Ó","Ô","Õ","Ö","Ø","Ù","Ú","|","\\","<",">","/","?","[","]","{","}","¡",'¢',"¤","¥","§","¨","©","ª","«","¯","°","±","²","³","µ","¶","·","¸","¹","º","»","¼","½","¾","¿","×"]
forte = ["ú","û","ü","ý","þ","ÿ","÷","Û","Ü","Ý","Þ","Ā","ā","Ă","ă","Ą","ą","Ć","ć","Ĉ","ĉ","Ċ","ċ","Č","č","Ď","ď","Ĕ","đ","Ē","ē","ĕ","Ė","ė","Ę","ę","Ě","ě","Ĝ","ĝ","Ğ","ğ","Ġ","ġ","Ģ","ģ","Ĥ","ĥ","Ħ","ħ","Ĩ","ĩ","Ī","ī","Ĭ","ĭ","Į","į","İ","ı","Ĳ","ĳ","Ĵ",'ĵ',"Ķ","ķ","ĸ","Ĺ","ĺ","Ļ","ļ","Ľ","ľ","Ŀ","ŀ","Ł","ł","Ń","ń","ņ","Ņ","Ň","ň","Ŋ","ŋ","Ō","ō","Ŏ"]
fortissimo = ["ŏ","Ő","ő","Œ","œ","Ŕ","ŕ","Ŗ","ŗ","Ř","ř","Ś","ś","Ŝ","ŝ","Ş","ş","Š","š","Ţ","ţ","Ť","ť","Ŧ","ŧ","Ũ","ũ","Ū","ū","Ŭ","ŭ","Ů","ů","Ű","ű","Ų","ų","Ŵ","ŵ","Ŷ","ŷ","Ÿ","Ź","ź","Ż","ż","Ž","ž","ſ","ƀ","Ɓ","Ƃ","ƃ","Ƅ","ƅ","Ɔ","Ƈ","ƈ","Ɗ","Ƌ","ƌ","ƍ","Ǝ","Ə","Ɛ","Ƒ","ƒ","Ɠ","Ɣ","ƕ","Ƙ","ƙ","ƚ","ƛ","Ɯ","Ɲ","ƞ","Ɵ","Ơ","ơ","Ƣ","ƣ","Ƥ","ƥ","Ʀ","Ƨ","ƨ","Ʃ"]
noteOff = ["ƪ","ƫ","Ƭ","ƭ","Ʈ","Ư","ư","Ʊ","Ʋ","Ƴ","ƴ","Ƶ","ƶ","Ʒ","Ƹ","ƹ","ƺ","ƻ","Ƽ","ƽ","ƾ","ƿ","Ǆ","ǅ","ǆ","Ǉ","ǈ","ǉ","Ǌ","ǋ","ǌ","Ǖ","ǖ","Ǘ","ǘ","Ǚ","ǚ","Ǜ","ǜ","ǝ","Ǟ","ǟ","Ǡ","ǡ","Ǣ","ǣ","Ǥ","ǥ","Ǧ","ǧ","Ǩ","ǩ","Ǫ","ǫ","Ǭ","ǭ","Ǯ","ǯ","Ƕ","Ȝ","ȝ","Ƞ","ȡ","Ȣ","ȣ","ṁ","ȴ","ȵ","ȶ","ȷ","ȸ","ȹ","Ⱥ","Ȼ","ȼ","Ƚ","Ⱦ","Ɂ","ɂ","Ƀ","Ʉ","Ʌ","Ɇ","ɇ","Ɉ","ɉ","Ɋ","Ɏ"]
pianoVel = '60'
mezzoforteVel = '50'
forteVel = '80'
fortissimoVel = '110'
noteOffVel = '0'

def finds(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def getList(dict):
    return list(dict.keys())


bosh = []
lengthOfPiece = 0
hghg = []
f = open("D:/Documents/Computer Science/Year 3/Final Project/1div.txt", encoding="utf-8")
data = f.read()
lengthOfPiece = len(data)
print(lengthOfPiece)
f.close()
with open("D:/Documents/Computer Science/Year 3/Final Project/1div.csv", "w", newline='') as g:
    csvOut = csv.writer(g)
    csvOut.writerow(['0', '0', 'Header', '1','1', '480'])
    csvOut.writerow(['1', '0', 'Start_track'])
    csvOut.writerow(['1', '0', 'Program_c', '0', '0'])
    for i in data:
        if i in piano:
            instances = finds(data, i)
            hghg.append(data.index(i))
            dsds = Counter(hghg)
            dgdg = dict(dsds)
            csvOut.writerow(['1',str(int(instances[dgdg[data.index(i)]-1])*10),'Note_on_c','0',piano.index(i)+minNote,pianoVel])
        elif i in mezzoforte:
            instances = finds(data, i)
            hghg.append(data.index(i))
            dsds = Counter(hghg)
            dgdg = dict(dsds)
            csvOut.writerow(['1',(instances[dgdg[data.index(i)]-1]),'Note_on_c','0',mezzoforte.index(i)+minNote,mezzoforteVel])
        elif i in forte:
            instances = finds(data, i)
            hghg.append(data.index(i))
            dsds = Counter(hghg)
            dgdg = dict(dsds)
            csvOut.writerow(['1',(instances[dgdg[data.index(i)]-1]),'Note_on_c','0',forte.index(i)+minNote,forteVel])
        elif i in fortissimo:
            instances = finds(data, i)
            hghg.append(data.index(i))
            dsds = Counter(hghg)
            dgdg = dict(dsds)
            csvOut.writerow(['1',(instances[dgdg[data.index(i)]-1]),'Note_on_c','0',fortissimo.index(i)+minNote,fortissimoVel])

        elif (i in noteOff):
            instances = finds(data, i)
            hghg.append(data.index(i))
            dsds = Counter(hghg)
            dgdg = dict(dsds)
            csvOut.writerow(['1',(instances[dgdg[data.index(i)]-1]),'Note_on_c','0',noteOff.index(i)+minNote,noteOffVel])

                        
    csvOut.writerow(['1', lengthOfPiece, 'End_track'])
    csvOut.writerow(['0', '0', 'End_of_file'])



    

