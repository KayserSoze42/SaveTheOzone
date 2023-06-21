from flask import Flask, render_template, request, redirect, url_for
from pytz import timezone
from datetime import datetime, timedelta

zones = [ 'America/Puerto_Rico', 'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific', 'US/Alaska', 'US/Hawaii', 'Europe/Bratislava']

zonesST = ['AST', 'EST', 'CST', 'MST', 'PST', 'AKST', 'HST', 'CEST']
zonesDT = ['ADT', 'EDT', 'CDT', 'MDT', 'PDT', 'AKDT', 'HST', 'CEDT']

statesA = ['Puerto Rico']
statesE = ['Connecticut', 'Delaware', 'Florida', 'Georgia', 'Indiana', 'Kentucky', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'New Hampshire', 'New Jersey', 'North Carolina', 'Ohio', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'Vermont', 'Virginia', 'Washington, DC', 'West Virginia', 'Indiana']
statesC = ['Alabama', 'Arkansas', 'Illinois', 'Iowa', 'Kansas', 'Louisiana', 'Minnesota', 'Mississippi', 'Missouri', 'Nebraska', 'North Dakota', 'Oklahoma', 'South Dakota', 'Tennessee', 'Texas', 'Wisconsin', 'Tennessee']
statesM = ['Arizona', 'Colorado', 'Idaho', 'Montana', 'New Mexico', 'New York', 'Utah', 'Wyoming']
statesP = ['California', 'Nevada', 'Oregon', 'Washington']
statesAK = ['Alaska']
statesH = ['Hawaii']

statesSpecial = ['Alaska', 'Arizona', 'Florida', 'Hawaii', 'Idaho', 'Indiana', 'Kansas', 'Kentucky', 'Michigan', 'Nebraska', 'North Dakota', 'Oregon', 'South Dakota', 'Tennessee', 'Texas']



app=Flask(__name__)

@app.route('/')
def home():

    startDate = ""
    startTime = ""
    endDate = ""
    endTime = ""
    outputFormat = ""
    inputZoneState = ""
    outputZoneState = ""
    stdt = ""

    dateFromPy = ""
    dateToPy = ""
    dateFromPyEnd = ""
    dateToPyEnd = ""

    if (not(request.args.get('startdate'))):
        ## Check now date and time, convert to output (BA BAU), set to params and redirect

        currentDate = datetime.now()

        startDate = str(currentDate.year) + "-" + padZero(currentDate.month) + "-" + padZero(currentDate.day)
        startTime = currentDate.strftime("%I:%M:%p")

        inputZoneState = "California"
        outputZoneState = "Bratislava"

        timezoneInput = timezone('US/Eastern')
        timezoneOutput = timezone('Europe/Bratislava')

        outputFormat = "24"

        dateFromPy = timezoneInput.localize(currentDate)
        dateToPy = dateFromPy.astimezone(timezoneOutput)

        if (dateFromPy.dst()):
            stdt = "1"
            dstTemp = 1
        else:
            stdt = "0"
            dstTemp = 0

        if (dateToPy.dst()):
            stdt = stdt + "1"
        else:
            stdt = stdt + "0"

        inpytText = dateFromPy.strftime("%Y-%m-%d %I:%M %p") + " " + inputZoneState

        return redirect(url_for('extendio', inpyt=inpytText, urlhome=request.base_url, urlozone=request.url_root+"/extendio", datestart=startDate, timestart=startTime, zonestateinput=inputZoneState, zonestateoutput=outputZoneState, formatoutput=outputFormat, stdt=stdt), code=307)

@app.route('/extendio')
def ozone():

    startDate = ""
    startTime = ""
    endDate = ""
    endTime = ""
    outputFormat = ""
    inputZoneState = ""
    outputZoneState = ""
    stdt = ""

    dateFromPy = ""
    dateToPy = ""
    dateFromPyEnd = ""
    dateToPyEnd = ""

    if (True):
        ## Convert and set from requested params 

        output = ""
        info = ""

        startDate = request.args.get('datestart')
        startTime = request.args.get('timestart')
        endDate = request.args.get('dateend')
        endTime = request.args.get('timeend')

        outputFormat = request.args.get('formatoutput')

        inputZoneState = request.args.get('zonestateinput')
        outputZoneState = request.args.get('zonestateoutput')

        stdt = request.args.get('stdt')

        ## Check if zone or state and apply relevant zones

        if (inputZoneState in zonesST):
            timezoneInput = timezone(zones[zonesST.index(inputZoneState)])

        elif (inputZoneState in zonesDT):
            timezoneInput = timezone(zones[zonesDT.index(inputZoneState)])

        else:
            if (inputZoneState in statesA):
                timezoneInput = timezone(zones[0])
            elif (inputZoneState in statesE):
                timezoneInput = timezone(zones[1])
            elif (inputZoneState in statesC):
                timezoneInput = timezone(zones[2])
            elif (inputZoneState in statesM):
                timezoneInput = timezone(zones[3])
            elif (inputZoneState in statesP):
                timezoneInput = timezone(zones[4])
            elif (inputZoneState in statesAK):
                timezoneInput = timezone(zones[5])
            elif (inputZoneState in statesH):
                timezoneInput = timezone(zones[6])
            else:
                timezoneInput = timezone(zones[7])

        if (outputZoneState in zonesST):
            timezoneOutput = timezone(zones[zonesST.index(outputZoneState)])

        elif (outputZoneState in zonesDT):
            timezoneOutput = timezone(zones[zonesDT.index(outputZoneState)])

        else:
            if (outputZoneState in statesA):
                timezoneOutput = timezone(zones[0])
            elif (outputZoneState in statesE):
                timezoneOutput = timezone(zones[1])
            elif (outputZoneState in statesC):
                timezoneOutput = timezone(zones[2])
            elif (outputZoneState in statesM):
                timezoneOutput = timezone(zones[3])
            elif (outputZoneState in statesP):
                timezoneOutput = timezone(zones[4])
            elif (outputZoneState in statesAK):
                timezoneOutput = timezone(zones[5])
            elif (outputZoneState in statesH):
                timezoneOutput = timezone(zones[6])
            else:
                timezoneOutput = timezone(zones[7])

        fromFormat = ""
        if (len(startTime) > 6):

            dateFromPy = datetime.strptime(startDate + " " + startTime, "%Y-%m-%d %I:%M:%p")
            fromFormat = "12"
        else:
            fromFormat = "24"

            try:
                dateFromPy = datetime.strptime(startDate + " " + startTime, "%Y-%m-%d %H:%M:")

            except:
                dateFromPy = datetime.strptime(startDate + " " + startTime, "%Y-%m-%d %H:%M")

        if (endDate):

            if (endTime):

                if (len(endTime) > 6):
                    dateFromPyEnd = datetime.strptime(endDate + " " + endTime, "%Y-%m-%d %I:%M:%p")

                else:
                    dateFromPyEnd = datetime.strptime(endDate + " " + endTime, "%Y-%m-%d %H:%M:")

        dateInPy = timezoneInput.localize(dateFromPy)
        if (dateFromPyEnd != ""):
            dateInPyEnd = timezoneInput.localize(dateFromPyEnd)

        dateOutPy = dateInPy.astimezone(timezoneOutput)
        if (dateFromPyEnd != ""):
            dateOutPyEnd = dateInPyEnd.astimezone(timezoneOutput)

        dstOne = 0
        if (dateInPy.dst()):
            dstOne = 1
        dstOneEnd = 0
        if (dateFromPyEnd != ""):
            if (dateInPyEnd.dst()):
                dstOneEnd = 1

        dstTwo = 0
        if (dateOutPy.dst()):
            dstTwo = 1

        info = setInfo(dstOne, dstTwo, inputZoneState, outputZoneState)

        info = info.split("!")


        infoA = ""
        infoB = ""
        infoC = ""
        infoD = ""
        if (len(info) == 4):
            infoA = info[3]
        if (len(info) >= 3):
            infoB = info[2]
        if (len(info) >= 2):
            infoC = info[1]
        if (len(info) >= 1):
            infoD = info[0]

        ## Check for toggled STDT and add delta hours if missing
        if (str(stdt[0]) == "0"):
            dateInPy = dateInPy - timedelta(hours=dstOne)

        if (str(stdt[1]) == "0"):
            dateOutPy = dateOutPy - timedelta(hours=dstTwo)

        ## Check if there's ending date and perform ==||==
        if (dateFromPyEnd != ""):
            if (str(stdt[0]) == "0"):
                dateInPyEnd = dateInPyEnd - timedelta(hours=dstOne)

            if (str(stdt[1]) == "0"):
                dateOutPyEnd = dateOutPyEnd - timedelta(hours=dstTwo)

            ## Check for Output Format and set Ticket Timeframe
            if (str(outputFormat) == "12"):
                output = dateOutPy.strftime("%Y-%m-%d %I:%M %p") + " >> " + dateOutPyEnd.strftime("%Y-%m-%d %I:%M %p") + " " + outputZoneState

            else:
                output = dateOutPy.strftime("%Y-%m-%d %H:%M") + " >> " + dateOutPyEnd.strftime("%Y-%m-%d %H:%M") + " " + outputZoneState

        ## If there's no ending date, set output with start only
        else:
            if (str(outputFormat) == "12"):
                output = dateOutPy.strftime("%Y-%m-%d %I:%M %p") + " " + outputZoneState

            else:
                output = dateOutPy.strftime("%Y-%m-%d %H:%M") + " " + outputZoneState

        if (dateFromPyEnd != ""):
            if (str(fromFormat) == "12"):
                inpytText = dateInPy.strftime("%Y-%m-%d %I:%M %p") + " >> " + dateInPyEnd.strftime("%Y-%m-%d %I:%M %p") + " " + inputZoneState
            else:
                inpytText = dateInPy.strftime("%Y-%m-%d %H:%M") + " >> " + dateInPyEnd.strftime("%Y-%m-%d %H:%M") + " " + inputZoneState

        else:
            if (str(fromFormat) == "12"):
                inpytText = dateInPy.strftime("%Y-%m-%d %I:%M %p") + " " + inputZoneState
            else:
                inpytText = dateInPy.strftime("%Y-%m-%d %H:%M") + " " + inputZoneState


        return render_template('home.html', urlhome=request.url_root, urlozone=request.base_url, datestart=startDate, timestart=startTime, zonestateinput=inputZoneState, zonestateoutput=outputZoneState, formatoutput=outputFormat, stdt=stdt, inpyt=inpytText, outpyt=output, pynfoa=infoA, pynfob=infoB, pynfoc=infoC, pynfod=infoD )

## Pad number with leading zero [ 0X ]
def padZero(num):
    return(f'{num:02}')

## Set info based on dst and zones
def setInfo(dstInput, dstOutput, zoneInput, zoneOutput):
    infoText = ""

    ## Check for special states regarding DST 
    if ((zoneInput == 'Hawaii' or zoneInput == 'HST' or zoneInput == 'Puerto Rico') or (zoneOutput == 'Hawaii' or zoneOutput == 'Puerto Rico')):

        infoText += " \r\n " + "Hawaii / Puerto Rico do not observe DS !"

    elif (zoneInput == 'Arizona' or zoneOutput == 'Arizona'):

        infoText += " \r\n " + "Arizona does not observe DS, except, of course, the Navajo Nation !"

    if (zoneInput in statesSpecial or zoneOutput in statesSpecial):
        
        if (zoneInput == 'Alaska' or zoneOutput == 'Alaska'):

            infoText += " \r\n " + "Alaska is in AKST and HST !"

        elif (zoneInput == 'Florida' or zoneOutput == 'Florida'):

            infoText += " \r\n " + "Florida is in CST and EST !"

        elif (zoneInput == 'Idaho' or zoneOutput == 'Idaho'):

            infoText += " \r\n " + "Idaho is in PST and MST !"

        elif (zoneInput == 'Indiana' or zoneOutput == 'Indiana'):

            infoText += " \r\n " + "Indiana is in EST and CST !"

        elif (zoneInput == 'Kansas' or zoneOutput == 'Kansas'):

            infoText += " \r\n " + "Kansas is in CST and MST !"

        elif (zoneInput == 'Kentucky' or zoneOutput == 'Kentucky'):

            infoText += " \r\n " + "Kentucky is in EST and CST !"

        elif (zoneInput == 'Michigan' or zoneOutput == 'Michigan'):

            infoText += " \r\n " + "Michigan is in EST and CST !"

        elif (zoneInput == 'Nebraska' or zoneOutput == 'Nebraska'):

            infoText += " \r\n " + "Nebraska is in CST and MST !"

        elif (zoneInput == 'North Dakota' or zoneOutput == 'North Dakota'):

            infoText += " \r\n " + "North Dakota is in CST and MST !"

        elif (zoneInput == 'Oregon' or zoneOutput == 'Oregon'):

            infoText += " \r\n " + "Oregon is in PST and MST !"

        elif (zoneInput == 'South Dakota' or zoneOutput == 'South Dakota'):

            infoText += " \r\n " + "South Dakota is in CST and MST !"

        elif (zoneInput == 'Tennessee' or zoneOutput == 'Tennessee'):

            infoText += " \r\n " + "Tennessee is in EST and CST !"

        elif (zoneInput == 'Texas' or zoneOutput == 'Texas'):

            infoText += " \r\n " + "Texas is in CST and MST !"

    if (dstInput == 1):
        infoText += " \r\n " + zoneInput + " observes DS at the specified date !"
    if (dstOutput == 1):
        infoText += " \r\n " + zoneOutput + " observes DS at the specified date !"

    return infoText


if __name__ ==  '__main__':
    app.run(debug=False, host='0.0.0.0', port='42069')
