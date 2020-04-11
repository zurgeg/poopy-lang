print('PoopyLang Runner 0.1.0.0')
#####
#import parser1_2 as parser
import sys
#If not on dev machine, use:
import parser
for i in open(sys.argv[1]).readlines():
    #print(i)
    prsd = parser.p.parse(i.strip())
    
    parser.PSTransformer().transform(prsd)
    
