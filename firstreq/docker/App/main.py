#!/usr/bin/python
import os
import psutil
import json
import falcon

# class cpuClass (object):
#       def on_get(self, req, res):
#           res.status = falcon.HTTP_200
#           res.body = (getCpuState())



def getCpuState():
    t = psutil.cpu_times_percent(percpu=False)
    cpu = t._asdict()
    # cpuData = {"system.cpu.idle" : cpu["idle"],
    #            "system.cpu.user" : cpu["user"],
    #            "system.cpu.guest" : cpu["guest"],
    #            "system.cpu.iowait" : cpu["steal"],
    #            "system.cpu.system" : cpu["system"]}
    return cpu

def getVmemState():
    vm = psutil.virtual_memory()
    # vMem= vm.__dict__    
    # return {"total" : vMem["total"], "used" : vMem["used"], "free" : vMem["free"], "shared" : vMem["shared"]}
    return vm._asdict()

def getSwapMem():
    swpmem = psutil.swap_memory()
    # swp = swpmem.__dict__
    # return {"total" : swp["total"], "used" : swp["used"], "free" : swp["free"]}
    return swpmem._asdict()

def getCombinedMemState():
    return {"virtual" : getVmemState(), "swap" : getSwapMem()}


def topCpu():
    c = [(p.pid, p.info['username'], p.info['name'] ,sum(p.info['cpu_times']))for p in sorted(psutil.process_iter(attrs=['name', 'cpu_times','username']),key=lambda p: sum(p.info['cpu_times'][:2]))][-3:]
    lst= list()
    for x in c:
        pr = {"pid" : 0, "username" : "", "name" : "", "cpu" : 0.0}
        pr["pid"] = x[0]
        pr["username"] = x[1]
        pr["name"] = x[2]
        pr["cpu"] = x[3]
        lst.append(pr)
    return lst


def callCpu():
    return json.dumps(getCpuState(), sort_keys=True, indent=2)

def callMem():
    return json.dumps(getCombinedMemState(),sort_keys=True, indent=2)

def callTopPocess():
    return json.dumps(topCpu(), sort_keys=True, indent=2) 


print(callCpu())
print(callMem())
print(callTopPocess())


class cpuRes(object):
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = (callCpu())


class memRes(object):
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = (callMem())


class topRes(object):
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = (callTopPocess())


app = falcon.API()

cpu = cpuRes()
mem = memRes()
top = topRes()

app.add_route("/cpu", cpu)
app.add_route("/memory", mem)
app.add_route("/top", top)






