#Code by Noah Tingbratt

import pykod.PET_Tmrt as so
import pykod.PET_calc as p
def petcalc(Ta, RH, Ws, year, month, day, hour,location,bodym,bodyh,age,clo,sex,pace_per_minute=16):     
    def calcTmrt(Ta, RH, year, month, day, hour,location):
        Fside,Fup,Fcyl = 0.22,0.06,0.28 #Ståendes vid Liggande:    Fside,Fup,Fcyl = 0.166666, 0.166666, 0.2
        Tmrt = so.Solweig1D_2020a_calc(Fside, Fup, Fcyl,location,Ta, RH, year, month, day, hour,minu=30)
        return float(Tmrt)
    def calcPet(Ta, RH, Ws, Tmrt,workperkilo=80):
        WsPET = (1.1 / 10) ** 0.2 * Ws #corretion from 10 meters height to 1.1 meters height 
        mbody, ht, clo, age, sex,vilowork = 75., 1.8, 0.9, 35,  1,0#[kg], [m], [1], [years], [W], [m 1/f 2]
        resultPET = p._PET(Ta, RH, Tmrt, WsPET, mbody, age, ht, max(workperkilo*mbody+vilowork,80), clo, sex) #get Pet
        return float(resultPET)   
    def pace(pacein):
        if pacein<=15:
            return 0
        if pacein <2.66:
             return 23*3.5
        paces=[15,11.84,9.81,9.10,8.29,7.31,6.60,6.06,5.57,5.33,4.97,4.66,4.34,4.14,3.93,3.73,3.39,3.11,2.87,2.66]
        metrates=[3,3.3,4.5,6.5,7.8,8.5,9,9.3,10.5,11,11.8,12,12.5,13,14.8,14.8,16.8,18.5,19.8,23]
        index=0
        while pacein>paces[index]:
            index+=1
        pacefactorn=(metrates[index-1]*(pacein-paces[index-1])+metrates[index]*(paces[index]-pacein))/(paces[index]-paces[index-1])
        return pacefactorn*3.5
    Tmrt = calcTmrt(Ta, RH, year, month, day, hour,location)
    work=pace(pace_per_minute)
    resultPET = calcPet(Ta, RH, Ws, Tmrt,bodym,bodyh,age,clo,sex,workperkilo=work)
    return Tmrt, resultPET
def index(form):
        Ta = float(form.get("Ta",20))        
        RH = float(form.get("RH",50))
        month = int(form.get("month",7))
        day = int(form.get("day",20))
        hour = int(form.get("hour",12))
        year = int(form.get("year",2025))
        location = {'latitude':float(form.get("latitude",57.691)), "longitude":float(form.get("longitude",11.977)), "altitude":int(form.get("altitude",45))}
        Ws = float(form.get("Ws",0))

        bodym= float(form.get("mass",80))
        bodyh= float(form.get("height",1.8))
        age=int(form.get("age",35))
        clo=float(form.get("clo",0.9))
        pace_per_minute=float(form.get("pace_per_minute",16))
        if form.get("gender","man").lower()=="man":
            sex=1
        else:
            sex=2
        
 
        
        if Ta > 70 or Ta < -100:
            print("petresult.html", "Unreasonable air temperature filled in",Ta)
        if RH > 100 or RH < 0:
            print("petresult.html", "Unreasonable relative humidity filled in")
        if month > 12 or month < 0:
            print("petresult.html","Incorrect month filled in")
        if day > 31 or day < 0:
            print("petresult.html","Incorrect day filled in")
        if hour > 23 or hour < 0:
            print("petresult.html","Incorrect hour filled in")
        if Ws > 100 or Ws < 0:
            print("petresult.html", "Unreasonable Wind speed filled in")
        
        # Main calculation
        if Ta is not None and RH is not None and Ws is not None:
            Tmrt, resultPET = petcalc(Ta, RH, Ws, year, month, day, hour,location,bodym,bodyh,age,clo,sex,pace_per_minute)
            return resultPET,Tmrt
