import sys, os
INTERP = os.path.join(os.environ['HOME'], '52.11.185.92', 'bin', 'python')
if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)
        sys.path.append(os.getcwd())

sys.path.append('mini_city')
from home import app as application                                      