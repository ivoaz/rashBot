from Util import U, sign, Range, Range180, ang_dif, regress


def controls(s):

    # s.throttle = regress((s.y-s.yv*.25*s.brakes)/900)
    s.throttle = regress((s.y-s.yv*(s.dT+.2*s.brakes))/900)
    s.steer = regress(s.a-s.av/40)
    s.pitch = regress(-s.i-s.iv/15)
    s.yaw = regress(s.a-s.av/12)
    s.roll = regress(-s.r+s.rv/22)*(abs(s.a)<.15)

    s.boost = (abs(s.a)<0.1 and abs(s.i)<0.25 and s.throttle>0.5 and 
               s.pyv<2250 and s.pB>.1)

    s.powerslide = s.jump = 0

    # general powerslide
    if (s.throttle*s.pyv>=0 and s.av*s.steer>=0 and 
       (ang_dif(s.a,s.pva,1)<.1 and s.x*s.pxv>=0 and abs(.5-abs(s.a))<.45 ) 
       or (.2<ang_dif(s.a,s.av/20,1)<.8 and abs(s.xv)<200 ) ) :
        s.powerslide=1

    # turn 180°
    if s.d2>400 and abs(s.a+s.av/2.25)>0.45 :
        if abs(s.a)>0.98: s.steer = 1
        if s.d2>700 and  s.pyv<-90 :
            if abs(s.a)<0.98 and abs(s.av)>0.5 : s.powerslide = 1
            s.steer = -sign(s.steer)
        elif s.d2>900 and abs(s.a)<0.95 and s.pyv<1000 :
            s.throttle = 1

    # three point turn
    if (s.poG and 20<abs(s.x)<400 and abs(s.y)<200 and .35<abs(s.a)<.65 
        and abs(s.pyv)<550 and abs(s.yv)<550 ):
        s.throttle = -sign(s.throttle)
        s.steer = -sign(s.steer) 

    # general jump
    if (s.z>140 and (
        # flying jump
        (s.z<Range((200*s.jcount+s.pB*5)*s.dT*2, 250*s.jcount+s.pB*9)
         and s.d2pv<120 and ang_dif(s.a,s.pva,1)<.05 ) or
        # directly below the ball
        (s.z<450 +s.pB*4 and s.d2<110 and s.vd2<150 ))):
            s.jumper = 1

    # jumping off walls
    if ((s.z>1350 or ((s.d<s.z*1.5 or s.vd<400) and s.pL[2]<500 
        and abs(s.a)<.15 and s.bL[2] < 500)) and s.poG and 
        s.pL[2]>60 and (abs(0.5-abs(s.a))>0.25 or s.d>2500)) or (
        s.poG and s.pL[2]>1900 and s.d2pv<120 )  : 
            s.jumper = 1

    # flip
    if (s.flip and s.d>400 and ang_dif(s.a,s.pva,1)<.06 and s.pB<80 
        and s.pvd<2200 and s.jcount>0 and (s.gtime>0.05 or not s.poG)
        and not s.jumper and ( (s.pyv>1640 and s.y-s.yv/4>3500 )
        or (abs(s.a)>0.75 and abs(s.y-s.yv/6)>850 and s.pyv<-140)
        or (s.pyv>1120 and s.y-s.yv/4>3000 and s.pB<16)
        or (2000>s.pyv>970 and s.y-s.pyv/4>1700 and s.pB<6) )) :
            s.dodge = 1
            s.xa = s.ta

    # jump for wavedash
    if (s.d>450 and 750<(s.y-s.yv/4) and ang_dif(s.a,s.pva,1)<.03
        and abs(s.i)<0.1 and s.pL[2]<50 and s.poG and s.pB<40 and 
        1050<s.pvd<2200 and s.gtime>.1 and s.wavedash):
        s.jump = 1

    # forward wavedash
    if (s.jcount>0 and s.pL[2]+s.pV[2]/20<32 and abs(s.r)<0.15 and 
        abs(s.a)<0.07 and s.y>400 and 0<abs(s.pR[0]/U)<0.12 and 
        not s.poG and s.pV[2]<-210 and s.wavedash ) :
        s.jump = 1
        s.pitch = abs(s.a)*2 -1
        s.yaw = s.roll = 0


    if s.shoot : 
        dodge_hit(s)


    # handling long jumps
    if s.jumper and s.jcount>0 :

        s.jump = 1

        if not s.poG and (s.ljump != s.lljump or not s.ljump) :
            s.pitch = s.yaw = s.roll = 0

        if 0.19<s.airtime and s.z+s.zv/11>120 : 
            s.jump = not s.ljump

    # handling pre-dodge 
    if s.dodge and s.jcount>0 :

        if s.poG :
            s.jump = 1
        else:
            s.jump = 0
            
        if 0.08<s.airtime and s.pL[2]>45 :
            s.jump = not s.ljump
            s.pitch = abs(s.xa)*2 -1
            s.yaw = (abs(Range180(s.xa+0.5,1)*2) -1)
            s.roll = 0
            s.djT = s.time

    # handling post-dodge
    if 0.05<s.djtime<0.25 :
        s.pitch = s.roll = s.yaw = 0

    if 0.25<s.djtime<0.65 :
        if abs(s.a)<0.5 : 
            if abs(s.a)<0.8: s.pitch = -sign(s.iv)
        else: s.pitch = s.yaw = s.roll = 0

    if not s.index: 0


def dodge_hit(s):
    # dodge hit
    if ( s.d2pv<90 and s.bd<900
        and abs(s.z)<150 and ang_dif(s.ta,s.pva,1)<0.7) :
        # dodge to shoot
        if (s.gtd<s.gpd and (abs(s.gaimdx)<300 or Range180(s.gta-s.gpa,1)<.03)
        # dodge to clear
         or (s.gtd>s.gpd and abs(s.ooglinex)>1100) 
        # dodge for 
         or s.kickoff ):
            s.dodge = 1; s.xa = s.ba