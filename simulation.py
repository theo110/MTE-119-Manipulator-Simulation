from cmath import inf
import math
 
 
def calc(l1,l2,l3,scenarioAngle, scenarioX, scenarioY):
    returnInfo = {
        "torque": 99999,
        "l1": l1,
        "l2": l2,
    }
    if(l1==0 or l2==0 or l3 ==0):
        return returnInfo
   
    Bx = scenarioX - l3*math.cos(scenarioAngle)
    By = scenarioY - l3*math.sin(scenarioAngle)
    d = math.sqrt(math.pow(Bx,2)+math.pow(By,2))
    tc = (math.pow(l2,2)-math.pow(l1,2)-math.pow(d,2))/(-2*l1*d)
    if(abs(tc)>1):
        return returnInfo
   
    theta = math.acos(tc)
    zeta = theta + math.atan2(By,Bx)
    if(zeta is not None):
        d1 = l1*math.cos(zeta)
    else:
        return returnInfo
   
    d2 = Bx - d1
    d3 = l3*math.cos(scenarioAngle)
 
    #finds distance of torques to origin
    dm1 = d1/2
    dm2 = d1 + d2/2
    dm3 = d1 + d2 + d3/2
 
    t1 = dm1 * 4 * 9.81 * l1
    t2 = dm2 * 2 * 9.81 * l2
    t3 = dm3 * 1 * 9.81 * l3
 
    tClaw = 5 * 9.81 * scenarioX
    tTotal = t1 + t2 + t3 + tClaw
 
    if By<0 or math.sin(zeta)<0:
        tTotal = 999999
    returnInfo = {
        "torque": tTotal,
        "l1": l1,
        "l2": l2,
    }
    return returnInfo
 
def findThiccT(l1,l2,l3):
    #Scenario 1
    Scenario1 = calc(l1,l2,l3,-60*math.pi/180,0.75,0.1)
 
    #Scenario 2
    Scenario2 = calc(l1,l2,l3,0*math.pi/180,0.5,0.5)
 
    #Scenario 3
    Scenario3 = calc(l1,l2,l3,45*math.pi/180,0.2,0.6)
    return math.sqrt(Scenario1["torque"]**2+Scenario2["torque"]**2+Scenario3["torque"]**2)

def simulate(min, max, iter):
   
    minT = float('inf')
    minI = 0
    minJ = 0
    minK = 0
    resultMatrix = []
    jump = (max-min)/float(iter)
    for i in range(min,iter+1):
        resultMatrix.append([])
        for j in range(min,iter+1):
            resultMatrix[i].append([])
            for k in range(min,iter+1):
                resultMatrix[i][j].append(findThiccT(i*jump,j*jump,k*jump))
                if(resultMatrix[i][j][k]<minT):
                    minT = resultMatrix[i][j][k]
                    minI = i*jump
                    minJ = j*jump
                    minK = k*jump
    res = {
        "minT": minT,
        "minI": minI,
        "minJ": minJ,
        "minK": minK,
    }
    return res
 
print(simulate(0,1,1000))
 
 

