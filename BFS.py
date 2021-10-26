import simpy
import numpy as np

number_of_ball = 1000 
number_of_bucket = 21 
SL_in_time = 20/14 # sec                                 
SL_out_time = 20 # sec                                   
BPu_out_time = 20/7 # sec                              
BPi_out_time = 20/14 - 0.000001 # sec                 
Wh_out_time = 20/7*9 - 0.0000001 # sec                 
BU_out_time = 20/14 - 0.00000001 # sec                
Con_out_time = 20/7*2 - 0.000000001 # sec                                                          
                                                     
BS_one_move = 20/7*9/10 # sec                         
BS_to_BE_time = BS_one_move*3 - 0.000001 # sec           
BE_empty_time = BS_one_move/2 # sec                     
BE_to_BS_time = BS_one_move - 0.2 # sec                  
BS2_out_time = BS_one_move*2 - 0.0000001 # sec          
BL_out_time = 20/7*6 - BS_one_move*6 - 0.00000001 # sec 
Ball_out_time = Wh_out_time + BU_out_time + Con_out_time + BS_to_BE_time + BE_empty_time # sec

# Spiral_Lift
def SL_in(env, store):
    i = 0
    for j in range(number_of_ball):
      yield env.timeout(SL_in_time)
      if np.random.rand() <= 0.95:
         ball_name = "ball {:2d}".format(i)
         yield Spiral_Lift.put(ball_name)
         i += 1
         sign1.put("msg")
         sign20.put("msg")
         print("{:6.2f} sec.  M1_in            : {}".format(env.now, ball_name))
      else:
         sign1.put("nope")
         sign20.put("nope")

def To_BPu(env, store):
        yield env.timeout(SL_out_time)
        item = yield Spiral_Lift.get()
        sign2.put("msg")
        print("{:6.2f} sec.  From M1 To M2-1  : {}".format(env.now, item))

def missing(env, store):
        yield env.timeout(SL_out_time)
        sign2.put("nope")

def SL_BPu(env, store, n):
    for i in range(n):
      msg1 = yield sign1.get()
      if msg1 == "msg":
         env.process(To_BPu(env, store))
      else:
         env.process(missing(env, store))

# Ball_Pusher
def BPu_in(env, store):
    i = 0
    for j in range(number_of_ball):
        msg2 = yield sign2.get()
        if msg2 == "msg":
           ball_name = "ball {:2d}".format(i)
           yield Ball_Pusher.put(ball_name)
           i += 1
        if j % 2 == 0:       
           sign3.put("msg")

def To_BPi(env, store):
      yield env.timeout(BPu_out_time)
      number = len(Ball_Pusher.items)
      if number == 2:                     
         item1 = yield Ball_Pusher.get()
         item2 = yield Ball_Pusher.get()
         print("{:6.2f} sec.  From M2-1 To M2-2: {}, {}".format(env.now, item1, item2))
         sign4.put("msg2")
      elif number == 1:                   
           item = yield Ball_Pusher.get()
           print("{:6.2f} sec.  From M2-1 To M2-2: {}".format(env.now, item))
           sign4.put("msg1")          

def BPu_BPi(env, store, n):
    for j in range(n):
        msg3 = yield sign3.get()
        if msg3 == "msg":
           env.process(To_BPi(env, store))

# Ball_Picker
def BPi_in(env, store):
    i = 0
    for j in range(number_of_ball):
        msg4 = yield sign4.get()
        if msg4 == "msg2":   
           for k in range(2):
               ball_name = "ball {:2d}".format(i)
               yield Ball_Picker.put(ball_name)
               i += 1
           sign5.put("msg")
        elif msg4 == "msg1":  
             ball_name = "ball {:2d}".format(i)
             yield Ball_Picker.put(ball_name)
             i += 1
             sign5.put("msg")                 

def To_Wh(env, store):
      yield env.timeout(BPi_out_time)
      number = len(Ball_Picker.items)
      if number == 2:
         item1 = yield Ball_Picker.get()
         item2 = yield Ball_Picker.get()
         print("{:6.2f} sec.  From M2-2 To M3  : {}, {}".format(env.now, item1, item2))
         sign6.put("msg2")
         sign21.put("msg2")
      elif number == 1:
           item = yield Ball_Picker.get()
           print("{:6.2f} sec.  From M2-2 To M3  : {}".format(env.now, item))
           sign6.put("msg1")         
           sign21.put("msg1")

def BPi_Wh(env, store, n):
    for i in range(n):
      msg5 = yield sign5.get()
      if msg5 == "msg":
         env.process(To_Wh(env, store))

# Wheel
def bucket(env, store):
    for j in range(number_of_ball):
        i = 1
        for k in range(number_of_bucket):
            msg6 = yield sign6.get()
            if msg6 == "msg1" or msg6 == "msg2": 
               bucket_name = "bucket {:2d}".format(i)
               yield Wheel.put(bucket_name)
               print("{:6.2f} sec.  bucket in M3     : {}".format(env.now, bucket_name))
               i += 1
               sign7.put("msg")

def To_BU(env, store):
    yield env.timeout(Wh_out_time)
    item = yield Wheel.get()
    print("{:6.2f} sec.  From M3 To M4    : {}".format(env.now, item))
    sign8.put("msg")

def Wh_BU(env, store, n):
    for i in range(n):
        msg7 = yield sign7.get()
        if msg7 == "msg":
           env.process(To_BU(env, store))

# Bucket_Unloader
def BU_in(env, store):
    for j in range(number_of_ball):
        i = 1
        for k in range(number_of_bucket):
            msg8 = yield sign8.get()
            if msg8 == "msg": 
               bucket_name = "bucket {:2d}".format(i)
               yield Bucket_Unloader.put(bucket_name)
               i += 1
               sign9.put("msg")

def To_Con(env, store):
    yield env.timeout(BU_out_time)
    item = yield Bucket_Unloader.get()
    print("{:6.2f} sec.  From M4 To M5-1  : {}".format(env.now, item))
    sign10.put("msg") 

def BU_Con(env, store, n):
    for i in range(n):
        msg9 = yield sign9.get()
        if msg9 == "msg":
           env.process(To_Con(env, store))

# Conveyor
def Con_in(env, store):
    for j in range(number_of_ball):
        i = 1
        for k in range(number_of_bucket):
            msg10 = yield sign10.get()
            if msg10 == "msg": 
               bucket_name = "bucket {:2d}".format(i)
               yield Conveyor.put(bucket_name)
               i += 1
               sign11.put("msg")

def To_BS(env, store):
    yield env.timeout(Con_out_time)
    item = yield Conveyor.get()
    print("{:6.2f} sec.  From M5-1 To M5-2: {}".format(env.now, item))
    sign12.put("msg") 

def Con_BS(env, store, n):
    for i in range(n):
        msg11 = yield sign11.get()
        if msg11 == "msg":
           env.process(To_BS(env, store))

# Bucket_Shifter
def BS_in(env, store):
    for j in range(number_of_ball):
        i = 1
        for k in range(number_of_bucket):
            msg12 = yield sign12.get()
            if msg12 == "msg": 
               bucket_name = "bucket {:2d}".format(i)
               yield Bucket_Shifter.put(bucket_name)
               i += 1
               sign13.put("msg")

def To_BE(env, store):
    yield env.timeout(BS_to_BE_time)
    item = yield Bucket_Shifter.get()
    print("{:6.2f} sec.  From M5-2 To M6  : {}".format(env.now, item))
    sign14.put("msg") 

def BS_BE(env, store, n):
    for i in range(n):
        msg13 = yield sign13.get()
        if msg13 == "msg":
           env.process(To_BE(env, store))

# Bucket_Emptier
def BE_in(env, store):
    for j in range(number_of_ball):
        i = 1
        for k in range(number_of_bucket):
            msg14 = yield sign14.get()
            if msg14 == "msg": 
               bucket_name = "bucket {:2d}".format(i)
               yield Bucket_Emptier.put(bucket_name)
               i += 1
               sign15.put("msg")

def To_BS2(env, store):
    yield env.timeout(BE_to_BS_time) 
    item = yield Bucket_Emptier.get()
    print("{:6.2f} sec.  From M6 To M5-2  : {}".format(env.now, item))
    yield env.timeout(BS_one_move - BE_to_BS_time) 
    sign16.put("msg") 

def BE_BS2(env, store, n):
    for i in range(n):
        msg15 = yield sign15.get()
        if msg15 == "msg":
           env.process(To_BS2(env, store))

# Ball_Exit
def Ball_in_Factory(env, store): 
    i = 0
    for j in range(number_of_ball):
        msg20 = yield sign20.get()
        if msg20 == "msg":
           ball_name = "ball {:3d}".format(i)
           yield Balls_in_Factory.put(ball_name)
           i += 1         

def Ball_out(env, store):
    yield env.timeout(Ball_out_time)
    msg22 = yield sign22.get()
    if msg22 == "msg2":
       item1 = yield Balls_in_Factory.get()
       item2 = yield Balls_in_Factory.get()
       yield Ball_Exit.put(item1)
       yield Ball_Exit.put(item2)
       print("{:6.2f} sec.  Balls_Out        : {}".format(env.now, Ball_Exit.items))
    elif msg22 == "msg1":
         item = yield Balls_in_Factory.get()
         yield Ball_Exit.put(item)
         print("{:6.2f} sec.  Balls_Out        : {}".format(env.now, Ball_Exit.items))

def Ball_Out(env, store, n):
    for i in range(n):
        msg21 = yield sign21.get()
        if msg21 == "msg2":      
           sign22.put("msg2")
           env.process(Ball_out(env, store))
        if msg21 == "msg1":   
           sign22.put("msg1")
           env.process(Ball_out(env, store))

# Bucket_Shifter2
def BS2_in(env, store):
    for j in range(number_of_ball):
        i = 1
        for k in range(number_of_bucket):
            msg16 = yield sign16.get()
            if msg16 == "msg": 
               bucket_name = "bucket {:2d}".format(i)
               yield Bucket_Shifter2.put(bucket_name)
               i += 1
               sign17.put("msg")

def To_BL(env, store):
    yield env.timeout(BS2_out_time)
    item = yield Bucket_Shifter2.get()
    print("{:6.2f} sec.  From M5-2 To M7  : {}".format(env.now, item))
    sign18.put("msg") 

def BS2_BL(env, store, n):
    for i in range(n):
        msg17 = yield sign17.get()
        if msg17 == "msg":
           env.process(To_BL(env, store))

# Bucket_Loader
def BL_in(env, store):
    for j in range(number_of_ball):
        i = 1
        for k in range(number_of_bucket):
            msg18 = yield sign18.get()
            if msg18 == "msg": 
               bucket_name = "bucket {:2d}".format(i)
               yield Bucket_Loader.put(bucket_name)
               i += 1
               sign19.put("msg")

def To_Wh2(env, store):
    yield env.timeout(BL_out_time)
    item = yield Bucket_Loader.get()
    print("{:6.2f} sec.  From M7 To M3    : {}".format(env.now, item))

def BL_Wh(env, store, n):
    for i in range(n):
        msg19 = yield sign19.get()
        if msg19 == "msg":
           env.process(To_Wh2(env, store))

env = simpy.Environment()
Spiral_Lift = simpy.Store(env, capacity=14)     # ball
Ball_Pusher = simpy.Store(env, capacity=2)      # ball
Ball_Picker = simpy.Store(env, capacity=2)      # ball
Wheel = simpy.Store(env, capacity=16)           # bucket
Bucket_Unloader = simpy.Store(env, capacity=1)  # bucket
Conveyor = simpy.Store(env, capacity=8)         # bucket
Bucket_Shifter = simpy.Store(env, capacity=4)   # bucket
Bucket_Emptier = simpy.Store(env, capacity=1)   # bucket
Bucket_Shifter2 = simpy.Store(env, capacity=2)  # bucket
Bucket_Loader = simpy.Store(env, capacity=1)    # bucket
Balls_in_Factory = simpy.PriorityStore(env, capacity=number_of_ball)
Ball_Exit = simpy.Store(env, capacity=number_of_ball)


sign1 = simpy.Store(env)
sign2 = simpy.Store(env)
sign3 = simpy.Store(env)
sign4 = simpy.Store(env)
sign5 = simpy.Store(env)
sign6 = simpy.Store(env)
sign7 = simpy.Store(env)
sign8 = simpy.Store(env)
sign9 = simpy.Store(env)
sign10 = simpy.Store(env)
sign11 = simpy.Store(env)
sign12 = simpy.Store(env)
sign13 = simpy.Store(env)
sign14 = simpy.Store(env)
sign15 = simpy.Store(env)
sign16 = simpy.Store(env)
sign17 = simpy.Store(env)
sign18 = simpy.Store(env)
sign19 = simpy.Store(env)
sign20 = simpy.Store(env)
sign21 = simpy.Store(env)
sign22 = simpy.Store(env)

env.process(SL_in(env, Spiral_Lift))
env.process(SL_BPu(env, Spiral_Lift, number_of_ball))
env.process(BPu_in(env, Ball_Pusher))
env.process(BPu_BPi(env, Ball_Pusher, number_of_ball))
env.process(BPi_in(env, Ball_Picker))
env.process(BPi_Wh(env, Ball_Picker, number_of_ball))
env.process(bucket(env, Wheel))
env.process(Wh_BU(env, Wheel, number_of_ball))
env.process(BU_in(env, Bucket_Unloader))
env.process(BU_Con(env, Bucket_Unloader, number_of_ball))
env.process(Con_in(env, Conveyor))
env.process(Con_BS(env, Conveyor, number_of_ball))
env.process(BS_in(env, Bucket_Shifter))
env.process(BS_BE(env, Bucket_Shifter, number_of_ball))
env.process(BE_in(env, Bucket_Emptier))
env.process(BE_BS2(env, Bucket_Emptier, number_of_ball))
env.process(BS2_in(env, Bucket_Shifter2))
env.process(BS2_BL(env, Bucket_Shifter2, number_of_ball))
env.process(BL_in(env, Bucket_Loader))
env.process(BL_Wh(env, Bucket_Loader, number_of_ball))
env.process(Ball_in_Factory(env, Balls_in_Factory))
env.process(Ball_Out(env, Ball_Exit, number_of_ball))


env.run(until=1000)
