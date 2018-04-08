import pyb
from ustruct import *
import uos
import array

ac = pyb.Accel()

freq = 120              # read frequency in Hz
dur = 4                 # flight duration in seconds
extra = 20              # extra frames before launch
l = freq*dur+extra      # desired amount of frames in data
countdown = l-extra     # number of frames to continue capturing after launch

launch = False          # boolean variable to store launch detection status

thres = 20              # threshold for launch detection

val = []                # current x y z time values
n = 0                   # index in cue
x = array.array('b',[0]*l)      # array for recorded x values
y = array.array('b',[0]*l)      # array for recorded y values
z = array.array('b',[0]*l)      # array for recorded z values
t = array.array('i',[0]*l)      # array for recorded time values

next = 0        # number of microseconds at which to capture data

logs = []       # list to store index of log files in
highest = 0     # int to store the highest filename-count in
no = 0          # int to store current filenamenumber in
filename = ''   # filename for logs


next = pyb.micros()
while True:
    while pyb.micros() < next:
        pass
    
    val = [ac.x(), ac.y(), ac.z(), pyb.micros()]     # could be merged
    x[n],y[n],z[n],t[n]=val                          # ^
    n = (n+1)%l
    next += round(1000000/freq)

    if not launch:
        try:
            av = sum(x[n-3:n-1]+y[n-3:n-1]+z[n-3:n-1])/9
        except:
            av = 0
        print(av)
        if abs(av) > thres:
            launch = True
    else:
        countdown -= 1
        if (countdown % 20 == 0):
            print(t[n-1])
        if countdown == 0:
            break

for q in range(n,l+n):
    i = q%l
    print(t[i],x[i],y[i],z[i])

# filenaming convention: log_[number].bin

def naming():
    logs = []
    highest = 0
    ls = uos.listdir()
#    print(ls)
    for k in range(0,len(ls)):
        if 'log_' in ls[k]:
            logs.append(ls[k].split('.')[0])

#    print(logs)
    for m in range(0,len(logs)):
        try:
            no = int(logs[m].split('_')[1])

        except:
            no = 0

#        print(no, highest)
        if no > highest:
            highest = no

#    print(highest)
    name = 'log_%s' % str(highest+1)
    return(name)    

filename = naming()
print(filename)

log = open('/flash/%s.bin' % filename, 'wb')
for p in range(n,l+n):
    j = p%l
    log.write(pack('3bi', x[j],y[j],z[j],t[j]))
log.close()
#print('data written to file called %s' % filename)
for q in range(n,l+n):
    i = q%l
    print(t[i],x[i],y[i],z[i],'\n')
