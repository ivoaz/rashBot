from Util import *
from Physics import approx_step, step, predict_sim


def strategy(s):

    s.flip = True
    s.wavedash = True

    s.aerialing = not s.poG and s.pL[2]>150 and s.airtime>.25
    s.kickoff = not s.bH and d3(s.bL)<99

    if s.kickoff : KickoffChase(s)
    else : ChaseBallBias(s)

    s.r = s.pR[2]/U

def ChaseBallBias(s):

    s.xv,s.yv,s.zv = s.pxv-s.bxv, s.pyv-s.byv, s.pzv-s.bzv
    s.vd,s.va,s.vi = spherical(s.xv,s.yv,s.zv)
    s.vd2 = d2([s.xv, s.yv])
    
    s.dT = Range( d3(s.pL+s.pV/9, s.bL+s.bV/9)/2700 + (.5-abs(abs(s.ba)-.5))/4, 5)

    s.dT = d3( step(s.bL,s.bV,s.baV,s.dT)[0], 
               step(s.pL,s.pV,s.paV,s.dT)[0] )/(2500-(not s.poG)*500)

    s.tL = predict_sim(s.bL,s.bV,s.baV,s.dT)[-1][0]

    if s.aerialing :
        s.tL = s.tL - approx_step(z3,s.pV,s.dT)[0] - s.pV*s.dT/2

    s.tx,s.ty,s.tz = local(s.tL,s.pL,s.pR)

    if s.pL[2]>50 and s.poG and (s.tL[2]<s.tz or s.tz>450+s.pB*9):
        s.tL[2]=93

    s.tx,s.ty,s.tz = local(s.tL,s.pL,s.pR)
    s.td,s.ta,s.ti = spherical(s.tx,s.ty,s.tz)

    aim(s)

    s.brakes = (abs(s.z)>80 or abs(s.a)>.1)

def KickoffChase(s):

    s.xv = s.pxv-s.bxv; s.yv = s.pyv-s.byv; s.zv = s.pzv-s.bzv
    s.vd,s.va,s.vi = spherical(s.xv,s.yv,s.zv)
    s.vd2 = d2([s.xv, s.yv])
    
    s.dT = .2

    s.tL = s.bL

    s.tx,s.ty,s.tz = local(s.tL,s.pL,s.pR)
    s.td,s.ta,s.ti = spherical(s.tx,s.ty,s.tz)

    aim(s)

    s.brakes = False

def aim(s):

    s.shoot = True

    togL = s.ogoal - s.tL
    tgL = s.goal - s.tL
    tpL = s.pL - s.tL

    s.gtL = -tgL
    s.gpL = s.pL - s.goal

    s.gtd,s.gta,s.gti = spherical(*s.gtL,0)
    s.gpd,s.gpa,s.gpi = spherical(*s.gpL,0)

    tpd,tpa,tpi = spherical(*tpL,0)

    if s.ogtd>s.ogpd  :

        gtd = s.gtd + 105

        tL = cartesian(gtd,s.gta,s.gti) + s.goal

    else :

        _,toga,togi = spherical(*togL,0)

        tL = cartesian(105, mid_ang(tpa,toga),togi) + s.tL

    s.tL = tL
    s.x,s.y,s.z = local(s.tL,s.pL,s.pR)
    s.d,s.a,s.i = spherical(s.x,s.y,s.z)

    s.d2 = d2([s.x,s.y])

    if not s.aerialing : 
        s.d2pv = d2([s.x-s.pxv*s.dT,s.y-s.pyv*s.dT])
    else: s.d2pv = s.d2


def closest_boost(s, tL):

    sdist = 0

    for i in range(34):
        bL = a3(s.game.gameBoosts[i].Location)
        Ac = s.game.gameBoosts[i].bActive
        dist = d3(bL, tL)
        if dist < sdist and Ac or sdist == 0 :
            sdist = dist
            L = bL

    return L

def GoTo(s, tL, brakes=True, shoot=False):

    s.brakes = brakes
    s.shoot = shoot

    s.tL = a3(tL)
    tL[2] = 50

    s.xv = s.pxv; s.yv = s.pyv; s.zv = s.pzv
    s.vd,s.va,s.vi = s.pvd,s.pva,s.pvi
    s.vd2 = d2([s.xv, s.yv])

    s.tx,s.ty,s.tz = local(s.tL,s.pL,s.pR)

    s.dT = Range(d3(s.pL + s.pV/5, s.tL)/2800, 5)

    if s.aerialing:
        s.tL = s.tL - approx_step(z3,s.pV,s.dT)[0]

    s.tx,s.ty,s.tz = local(s.tL,s.pL,s.pR)
    s.td,s.ta,s.ti = spherical(s.tx,s.ty,s.tz)

    s.x,s.y,s.z = s.tx,s.ty,s.tz
    s.d,s.a,s.i = s.td,s.ta,s.ti

    s.d2pv = d2([s.x-s.pxv*s.dT,s.y-s.pyv*s.dT])
    s.d2 = d2([s.x,s.y])
