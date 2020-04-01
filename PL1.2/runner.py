print('PoopyLang Runner 0.1.0.0')
#import parser1_2 as parser
import sys
#If not on dev machine, use:
import parser
for i in open(sys.argv[1]).readlines():
    prsd = parser.p.parse(i)
    
    parser.PSTransformer().transform(prsd)
    
