#!/usr/local/bin/python

import MySQLdb,getopt,sys

TAG="MYSQL_CONNECTIONS_CHECK"
def ok(stat):
    print TAG,"OK -",stat
    sys.exit(0)
    
def warn(stat):
    print TAG,"WARN -",stat
    sys.exit(1)
    
def critical(stat):
    print TAG,"CRITICAL -",stat
    sys.exit(2);

def main():
try:
opts,args = getopt.getopt(sys.argv[1:], "s:u:p:",["help", "output="])
except getopt.GetoptError, err:
print str(err)
sys.exit(2)

srv=''
usr=''
pwd=''
for o, a in opts:
if o == "-s":
srv = a
elif o == "-u":
usr = a
elif o == "-p":
pwd = a
else:
assert False, "unhandeled option"

if len(srv) == 0 or len(usr) == 0 or len(pwd) == 0:
critical('Missing arguments!')

db = MySQLdb.connect(host=srv,user=usr,passwd=pwd)
cursor = db.cursor()
cursor.execute("SELECT @@max_connections")
res = cursor.fetchall()
mCon = int(res[0][0])

cursor.execute("show status like '%Threads_connected%'")
res = cursor.fetchall()
cCon = int(res[0][1])

perUsed=(1.00*cCon/mCon*100)
perFree=100-perUsed

if perUsed > 90:
critical("Current mySQL connections exceeds 90%% currently %s" %perUsed)
elif perUsed > 75:
warn("Current mySQL connections exceeds 75%% currently %s" %perUsed)
else:
stat = "| max_connections=%s;0; threads_connected=%s;0;" % (mCon,cCon)
ok("All is well currently using %s%% of max_connections %s " %(perUsed,stat))

if __name__ == "__main__":
main()
