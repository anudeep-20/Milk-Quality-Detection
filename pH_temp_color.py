import serial, time
import datetime
import pymysql as pms

data = serial.Serial("COM4" , 9600 ,timeout = 0.1)
data.flush()

connection = pms.connect("localhost" ,"root" , "","quality_inf")
curs = connection.cursor()
##curs.execute("TRUNCATE TABLE milk_quality")

pH_arr = [0]*10
pH_myArr = [0]*10
temp_arr = [0]*10
R_arr = [0]*10
G_arr = [0]*10
B_arr = [0]*10
thres = 10
isWater = False

ID = int(raw_input("Enter Milk Man ID : "))

def time_unit(tu):
    tu = tu.split(' ')
    return ((int(tu[0].split('-')[2]))*86400 + (int(tu[1].split(':')[0]))*3600 + (int(tu[1].split(':')[1]))*60 + float(tu[1].split(':')[2]))

def around(R,G,B):
    ##(255,247,215),(219,214,171)

    diff_R = abs(255 - R)
    diff_G = abs(255 - G)
    diff_B = abs(255 - B)

    if(diff_R <= thres and diff_B <= thres and diff_B <= thres):
        return 0

    diff_R = abs(255 - R)
    diff_G = abs(247 - G)
    diff_B = abs(215 - B)

    if(diff_R <= thres and diff_B <= thres and diff_B <= thres):
        return 1    
    
    diff_R = abs(219 - R)
    diff_G = abs(214 - G)
    diff_B = abs(171 - B)

    if(diff_R <= thres and diff_B <= thres and diff_B <= thres):
        return 2

    return 3

def pH_water(pH_arr):
    time_now = time_unit(str(datetime.datetime.now()))
    
    if (time_now - time_init) <= 10:
        return '-s'
    if ((time_now - time_init) >= 10 and (time_now - time_init) <= 50):
        return str(sum(pH_arr)/float(len(pH_arr))) + '-t'
    if (time_now - time_init) >= 50:  
        return '-f'

LR = float(raw_input("Place the Lactometer in Milk and wait for 15 Seconds. Enter the reading : "))

print "First place the pH sensor in Milk for 15 seconds"
time.sleep(15)
print "Now place pH sensor in Water."
time.sleep(20)
isWater = True
time_init = time_unit(str(datetime.datetime.now()))
            
while True :
    if(data.inWaiting() > 0):
        myData = data.readline() 
        myData = myData.strip('\n')
        myData = myData.strip('\r')

        myData = myData.split(';')
        #print myData

        try :
            if myData[0] == '' :
                continue            
            if len(myData) >= 4:
                if myData[2].split('*')[2] == '':
                    continue
            if len(myData) < 4:
                continue
            
        except IndexError:
            continue
        
        #print myData

        try:
            pH = float(myData[0].split(',')[1].split(':')[1])
            pH_arr.append(pH)
            pH_arr = pH_arr[-10:]
            #print "pH_arr : ", pH_arr

            if pH_water(pH_arr).split('-')[1] == 'f':
                if (isWater == True):
                    print "The reference pH has been set. Now place the pH sensor in MILK..!!"
                    time.sleep(15)
                    isWater = False
            
            if pH_water(pH_arr).split('-')[1] == 't':
                pH_ref = float(pH_water(pH_arr).split('-')[0])

            if pH_water(pH_arr).split('-')[1] == 'f':
                #print pH_ref
                pH_myArr.append(pH + (7-pH_ref))
                pH_myArr = pH_myArr[-10:]
        
            print pH_myArr

        except (IndexError or TypeError):
            pass

        try:
            temp = myData[1].split(',')[1].split(':')[1]
            temp_arr.append(float(temp))
            temp_arr = temp_arr[-10:]
            if(temp_arr[9] == 15.5):
                CLR = LR
            else:
                CLR = LR + (int(temp_arr[9] - 15.5))*0.2

            print "CLR: " ,CLR
                
        except IndexError or ValueError:
            pass

        try:
            color = myData[2].split('*')
            if int(color[0]) >= 255:
                color[0] = 255
            if int(color[0]) < 0:
                color[0] = 0
            R_arr.append(int(color[0]))
            R_arr = R_arr[-10:]

            if int(color[1]) >= 255:
                color[1] = 255
            if int(color[1]) < 0:
                color[1] = 0
            G_arr.append(int(color[1]))
            G_arr = G_arr[-10:]

            if int(color[2]) >= 255:
                color[2] = 255
            if int(color[2]) < 0:
                color[2] = 0            
            B_arr.append(int(color[2]))
            B_arr = B_arr[-10:]

            qual = around(R_arr[9],G_arr[9],B_arr[9])
            print "qual: ",qual
        except IndexError :
            pass

        time_now = time_unit(str(datetime.datetime.now()))
    
        if (time_now - time_init) >= 90:
            print "----------Complete Analysis----------"

            time_now = str(datetime.datetime.now())

            if pH_myArr[9] <= 6.8 and pH_myArr[9] >= 6.4:
                pH = 0
                print "Milk pH : Good"        
            if pH_myArr[9] >= 6.8:
                pH = 1
                print "Milk pH : Alkaline"
            if pH_myArr[9] <= 6.4:
                pH = 2
                print "Milk pH : Acidic"

            print "CLR = ", CLR

            if qual == 0:
                print "Milk color is good"
            if qual == 1:
                print "Milk color is ok and it is in the process of spoilage"
            if qual == 2:
                print "Milk color is not good"
            if qual == 3:
                print "It is not Milk or It is a bad quality Milk"

            if (CLR >= 30 and CLR <=34):
                LR_n = 0
                print "Water is not mixed with the MILK."
            if (CLR <= 30):
                LR_n = 1
                print "Water is mixed with the MILK."
            if (CLR <= 22):
                LR_n = 2
                print "Large amount of Water is mixed with the MILK."
            if (CLR >= 34):
                LR_n = 3
                print "Other substances are mixed with milk to Increase its density."
            
            if (qual == 0 and pH == 0 and LR_n == 0):
                total_grade = 'A'
                print "Milk is perfectly suitable for Infants"
            if (qual == 1 and pH == 0 and LR_n == 0):
                total_grade = 'C'
                print "Milk is good but not suitable for Infants"
            if ((qual == 1 or qual == 0) and pH == 0 and LR_n == 1):
                total_grade = 'B'
                print "Milk cannot be used for drinking."
            if ((qual == 2 or qual == 3) or pH != 0 or (LR_n == 2 or LR_n == 3) ):
                total_grade = 'D'
                print "Worst quality of milk. It should be thrown."

            curs.execute("INSERT INTO milk_quality(Time,Milk_Man_ID,pH_Reading,Colour_Grade,Temperature,LR,CLR,Total_Grade) VALUES('"+str(time_now)+"',"+str(ID)+","+str(pH_myArr[9])+","+str(qual)+","+str(temp_arr[9])+","+str(LR)+","+str(CLR)+",'"+str(total_grade)+"');")
            connection.autocommit(True)

            print "----------------------------------------"
            break
