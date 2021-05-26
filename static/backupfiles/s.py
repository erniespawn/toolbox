# s.py
#!/usr/bin/python
import subprocess

cmd_list = ['uname -r', 'uptime']

out = []
err = []

for cmd in cmd_list:
    args = cmd.split()
    proc = subprocess.Popen(args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()
    out.append(stdoutdata)
    err.append(stderrdata)

print 'out=',out
print 'err=',err
