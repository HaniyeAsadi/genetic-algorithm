import random
import time
import sys

start_time = time.time()
N=100
print("اگر حین اجرای برنامه به خطای تقسیم بر صفر برخوردید، چندبار دیگر هم اجرا کنید تا جواب دیگری بدهد. چون توابع رندوم هستند، احتمال تقسیم بر صفر هم وجود دارد :))\n")

var_n = input("Enter number of variables you want: ")
operators = ['+', '-', '*', '/']
Generations = {}
Best_Fitness = sys.float_info.max
Best_equation =''
function = ''
variables = []
PointsValues = {}
if(int)(var_n) == 1:
    function = "x**2 + 15"
    variables.append("x")
    for i in range(1,100):
        tple1 = ()
        tple1 += (i, )
        PointsValues[tple1] = (tple1, round(eval(function, {"x" : tple1[0]}), 2))

if(int)(var_n)==2:
    function = "x + 10*y - 4*x"
    variables.extend(["x", "y"])

    for i in range(1,10):
        for j in range(1, 10):
            tple2 = ()
            tple2 += (i, j, )
            PointsValues[tple2] = (tple2, round(eval(function, {"x" : tple2[0], "y" : tple2[1]}), 2))

if(int)(var_n)==3:
    function = "x -y + 2*z - 4"
    variables.extend(["x", "y", "z"])
    for i in range(1,10, 2):
        for j in range(1, 10):
            for k in range(1,5):
                tple3 = ()
                tple3 += (i, j, k, )
                PointsValues[tple3] = (tple3, round(eval(function, {"x" : tple3[0], "y" : tple3[1], "z" : tple3[2]}), 2))

print("Function is : " + function)
g=0
Generations[g] = (g, )
for i in range(N): 
    function = ''
    m = random.randint(1,10)
    for j in range(m):
        function += str(random.randint(1, 20))
        op = random.choice(operators)
        function += op
        function += random.choice(variables)
        if j != m-1:
            Op = random.randint(0, 3)
            function += operators[Op]
    Generations[g] += (function, )

def function_Values(Generation, Points):
    global Best_Fitness, Best_equation
    fitness = []
    for i in range(1, len(Generation)):
        Values = []
        if((int)(var_n)==1):
            for j in Points:
                val = round(eval(str(Generation[i]), {"x" : j[0]}), 2)
                Values.append(val)
        if((int)(var_n)==2):
            for j in Points:
                val = round(eval(str(Generation[i]), {"x" : j[0], "y" : j[1]}), 2)
                Values.append(val)
        if((int)(var_n)==3):
            for j in Points:
                val = round(eval(str(Generation[i]), {"x" : j[0], "y" : j[1], "z" : j[2]}), 2)
                Values.append(val)
        fitness.append(round(MSE_value(main_values= Points, gen_values= Values), 5))
    
    m = min(fitness)
    if(m < Best_Fitness):
        Best_Fitness = m
        idx = fitness.index(m)
        Best_equation = Generation[idx+1]

    return fitness

def MSE_value(main_values, gen_values):
    Summation =0
    for i in range(len(main_values)):
        temp = list(main_values.items())[i]
        Summation += (float(temp[1][1]) - float(gen_values[i]))**2

    MSE = round(Summation / len(main_values), 7)
    return MSE

def Roulette(fitness):
    probablity = []
    temp = [round((float)(1/val), 7) for val in fitness]
    total = sum(temp)
    for j in range(len(temp)):
        probablity.append(round(temp[j] / total , 7))
    return probablity

def mutation():
    flag = False
    f = random.random()
    if(f < 0.0005):
        flag = True
    else:
        flag = False
    return flag

def ChooseTwo(wheel):
    bounds = []
    for i in range(len(wheel)):
        if i==0: 
            bounds.append(wheel[i])
        else :
            b = wheel[i] + bounds[-1]
            bounds.append(b)

    a = random.random()
    b = random.random()
    t = ()
    for i in range(len(bounds)):
        if bounds[i] > a :
            t += (i, )
            break

    for i in range(len(bounds)):
        if bounds[i] > b :
            t += (i, )
            break

    if t[0] == t[1]:
        my_list = list(t)
        while(my_list[0] == my_list[1]):
            b = random.random()
            for j in range(len(bounds)):
                if b < bounds[j] :
                    my_list[1] = j  
                    j = len(bounds)
        t = tuple(my_list)                  
    return t

def Crossover(chosen_idxs, generation):
    Children = ()
    global parent1, parent2, child1, child2, p1_first, p1_second, p2_first, p2_second, p1_break, p2_break
    p1 = chosen_idxs[0]
    p2 = chosen_idxs[1]
    ps=0
    for i in range(len(generation)):
        if i-1 == p1:
            parent1 = generation[i]
            ps+=1
        if i-1 == p2:
            parent2 = generation[i]
            ps+=1
        if ps==2:
            break
    
    p1_ops=0
    p2_ops=0
    for k in parent1:
        if(k in operators):
            p1_ops+=1

    for l in parent2:
        if(l in operators):
            p2_ops+=1

    if(p1_ops==0):
        p1_break = len(parent1)
    if(p2_ops==0):
        p2_break = len(parent2)
    if(p1_ops !=0 or p2_ops != 0):
        if(p1_ops!=0):
            p1_break = random.randint(1, p1_ops)
        if(p2_ops !=0):
            p2_break = random.randint(1, p2_ops)

    tmp1=0
    tmp2=0
    for m in range(len(parent1)):
        if(parent1[m] in operators):
            tmp1+=1
        if tmp1 == p1_break:
            p1_first = parent1[0:m+1]
            p1_second = parent1[m+1:len(parent1)]
            break 
    
    for o in range(len(parent2)):
        if(parent2[o] in operators):
            tmp2 +=1
        if tmp2 == p2_break:
            p2_first = parent2[0:o+1]
            p2_second = parent2[o+1:len(parent2)] 
            break 

    child1 = p1_first + p2_second
    Children += (child1, )
    if(mutation):
        child2 = p2_first[:len(p2_first)-1]
    else:
        child2 = p2_first + p1_second
    Children += (child2, )
    return Children

flag = False
for gen in range(20):
    fitnessValues = function_Values(Generations[g], PointsValues)
    roulette_wheel = Roulette(fitness= fitnessValues)
    Best_Fitness = min(fitnessValues)
    Best_equation = Generations[g][fitnessValues.index(Best_Fitness)+1]
    Generations[g+1] = (g+1, )
    if Best_Fitness < 10:
        flag = True
    for i in range(N + 40):
        if flag :
            i = N+40
        chosen_idx = ChooseTwo(wheel= roulette_wheel)
        child = Crossover(chosen_idxs= chosen_idx, generation= Generations[g])
        Generations[g+1] += (child[0], child[1], )
    g+=1
    if(flag):
        gen=100
        break

print("In Generation " + str(g) + ", I found the equation : " + Best_equation + " and the Best fitness over Generations equals to : " + str(Best_Fitness))
print("Total time : %s seconds" %round((time.time()-start_time), 3))