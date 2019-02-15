from .models import Shifts#Employees
#from django.contrib.auth.models import User
from datetime import datetime

Shifts = Shifts.objects.all().filter(Active=False)


def getTableHeader(DayNo):
    WeekTH = ['Shift Times']
    #OrderedShiftsByStartDate = Shifts.objects.all().order_by('Start')
    OrderedShiftsByStartDate = Shifts.order_by('Start')

    for i in range(DayNo, DayNo+7):
        FilteredShifts = OrderedShiftsByStartDate.filter(Start__day=i)
        if FilteredShifts:
            if FilteredShifts[0].Start.strftime('%a %d %b %Y') not in WeekTH:
                WeekTH.append(FilteredShifts[0].Start.strftime('%a %d %b %Y'))

    return WeekTH


def CreateTableHeadersList():
    Week1TH = getTableHeader(1)
    Week2TH = getTableHeader(8)
    Week3TH = getTableHeader(15)
    Week4TH = getTableHeader(22)
    Week5TH = getTableHeader(29)
    return [Week1TH, Week2TH, Week3TH, Week4TH, Week5TH]


def getShiftTimes(DayNo):
    WeekShifts = []
    TempShiftsTimeList = []
    #FilteredShifts = Shifts.objects.all().filter(Start__day__gte=DayNo,Start__day__lt=DayNo+8)#(Start__day=range(DayNo, DayNo + 8))
    FilteredShifts = Shifts.filter(Start__day__gte=DayNo,
                                                 Start__day__lt=DayNo + 8)  # (Start__day=range(DayNo, DayNo + 8))
    for i in FilteredShifts:
        iStartTime = datetime.strftime(i.Start, '%H:%M')
        iEndTime = datetime.strftime(i.End, '%H:%M')
        iShiftTime = [iStartTime, iEndTime]
        if iShiftTime not in TempShiftsTimeList:
            WeekShifts.append([i.Start, i.End])
            TempShiftsTimeList.append(iShiftTime)
    return WeekShifts


def CreateShiftTimesList():
    Week1Shifts = getShiftTimes(1)
    Week2Shifts = getShiftTimes(8)
    Week3Shifts = getShiftTimes(15)
    Week4Shifts = getShiftTimes(22)
    Week5Shifts = getShiftTimes(29)
    return [Week1Shifts, Week2Shifts, Week3Shifts, Week4Shifts, Week5Shifts]


def CreateWeekShiftList(WeekNo, TableHeaders, ShiftTimes):
    WeekShiftList = []
    for Shift in ShiftTimes[WeekNo]:
        ShiftStartTimeString = str(datetime.strftime(Shift[0], '%H:%M'))
        ShiftEndTimeString = str(datetime.strftime(Shift[1], '%H:%M'))
        ShiftTimeString = ShiftStartTimeString + ' - ' + ShiftEndTimeString
        WeekShiftListRow = [ShiftTimeString]
        SkipFirstItteration = True
        for Date in TableHeaders[WeekNo]:
            if SkipFirstItteration == True:
                SkipFirstItteration = False
                continue
            Date = datetime.strptime(Date, '%a %d %b %Y')
            Date = datetime.strftime(Date, '%d%m%Y')
            ShiftStartDateTime = datetime.strptime(Date+ShiftStartTimeString, '%d%m%Y%H:%M')
            ShiftEndDateTime = datetime.strptime(Date+ShiftEndTimeString, '%d%m%Y%H:%M')

            try:
                ShiftObject = Shifts.get(Start=ShiftStartDateTime, End=ShiftEndDateTime)
                WeekShiftListRow.append(ShiftObject.Employees.user.username)
            except:
                WeekShiftListRow.append(' ')
                #print('Get Username Failed: No Employee Assigned To Shift')
        WeekShiftList.append(WeekShiftListRow)
    return WeekShiftList


def CreateMonthShiftList():
    ShiftTimes = CreateShiftTimesList()
    TableHeaders = CreateTableHeadersList()
    Week1ShiftList = CreateWeekShiftList(0, TableHeaders, ShiftTimes)
    print(Week1ShiftList)
    Week2ShiftList = CreateWeekShiftList(1, TableHeaders, ShiftTimes)
    Week3ShiftList = CreateWeekShiftList(2, TableHeaders, ShiftTimes)
    Week4ShiftList = CreateWeekShiftList(3, TableHeaders, ShiftTimes)
    Week5ShiftList = CreateWeekShiftList(4, TableHeaders, ShiftTimes)
    return [Week1ShiftList, Week2ShiftList, Week3ShiftList, Week4ShiftList, Week5ShiftList], TableHeaders