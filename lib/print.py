from lib.colors import bcolors

def iprint(txt: str,color : str,status : str) :
    print("[",color,status,bcolors.ENDC ,"]",txt)
    
    
        