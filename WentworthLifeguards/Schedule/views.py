from .models import Employees, Shifts
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationPart1, UserRegistrationPart2, RemoveUser, AddShifts, RemoveShift
from .forms import SetAvailability, CancelAvailability
from datetime import datetime
from .GenerateRota import CreateMonthShiftList
from .GenerateSampleRota import CreateMonthShiftList as CreateProvisionalMonthShiftList
from .GenerateSchedule import getSchedule


def index(request):
    context = None
    return render(request, './Schedule/index.html', context)


@login_required(login_url='login')
def manage(request):

    ShiftsAvailable = Employees.objects.get(user=request.user).Availability.all()
    ShiftsAvailableList = []
    for i in ShiftsAvailable:
        print(i)
        String = str(i.Start.strftime('%d/%m/%Y %H:%M') + ' - ' + i.End.strftime('%d/%m/%Y %H:%M'))
        ShiftsAvailableList.append(String)

    print(ShiftsAvailableList)


    def ReturnPageAndContext(requestUser):
        EmployeeData = Employees.objects.get(user=requestUser)

        if EmployeeData.isManager:
            context = {'UserRegPt1': UserRegistrationPart1, 'UserRegPt2': UserRegistrationPart2,
                       'UserRemove': RemoveUser(requestUser), 'ShiftAdd':AddShifts(), 'ShiftRemove':RemoveShift,
                       'LockRota':''}
            page = './Schedule/adminmanage.html'
            return page, context
        else:
            context = {'SetAvailability':SetAvailability,
                       'ShiftsAvailable':ShiftsAvailableList, 'CancelAvailability':CancelAvailability(user=requestUser)}
            page = './Schedule/staffmanage.html'
            return page, context


    if request.method == 'POST':
        if "Create User" in request.POST:
            UserReg1 = UserRegistrationPart1(request.POST)
            UserReg2 = UserRegistrationPart2(request.POST)
            print('UserReg Forms 1')
            if UserReg1.is_valid() and UserReg2.is_valid():
                print('UserReg Forms 2')
                Username = UserReg1.cleaned_data['username']
                UserReg1.save()
                EmployeePhoneNumber = UserReg2.data['PhoneNo']

                UserReg2.save()
                EmployeeObject = Employees.objects.get(PhoneNo=EmployeePhoneNumber)
                print(Username)
                print(User.objects.get(username=Username))
                EmployeeObject.user = User.objects.get(username=Username)
                print(EmployeeObject.user)
                EmployeeObject.save()

                page, context = ReturnPageAndContext(request.user)
                return render(request, page, context)

        elif "Remove User" in request.POST:
            print('User Remove Forms')
            Username = request.POST['username']
            UserObject = User.objects.get(username=Username)
            UserObject.delete()

            page, context = ReturnPageAndContext(request.user)
            return render(request, page, context)

        elif "Add Shift" in request.POST:
            AddShiftsInstance = AddShifts(request.POST)
            if AddShiftsInstance.is_bound:
                print('Is Bound')
            else:
                print('Not bound')
                print(request.POST)
            print(AddShiftsInstance.errors)
            if AddShiftsInstance.is_valid():
                print('Add Shift Valid')
                Days = AddShiftsInstance.cleaned_data['Days']
                Month = AddShiftsInstance.cleaned_data['Month']
                Year = AddShiftsInstance.cleaned_data['Year']
                StartTime = AddShiftsInstance.cleaned_data['StartTime']
                EndTime = AddShiftsInstance.cleaned_data['EndTime']
                for Day in Days:
                    Day = str(Day).zfill(2)
                    StartDatetimeStr = str(Day) + str(Month) + str(Year) + str(StartTime.strftime('%H:%M'))
                    print(StartDatetimeStr)
                    StartDatetime = datetime.strptime(StartDatetimeStr, '%d%m%Y%H:%M')
                    EndDatetimeStr = str(Day) + str(Month) + str(Year) + str(EndTime.strftime('%H:%M'))
                    EndDatetime = datetime.strptime(EndDatetimeStr, '%d%m%Y%H:%M')
                    Shifts.objects.create(Start=StartDatetime, End=EndDatetime, Employees=None, Active=False)
                page, context = ReturnPageAndContext(request.user)
                return render(request, page, context)
            print('Add Shift Invalid')

        elif 'Remove Shift' in request.POST:
            print('Remove Shift Form')
            RemoveShiftInstance = RemoveShift(request.POST)
            FilteredShifts = Shifts.objects.all()
            if RemoveShiftInstance.is_valid():
                print('Remove Shift Is Valid')
                ShiftID = RemoveShiftInstance.cleaned_data['ShiftID']
                ShiftObject = FilteredShifts.get(pk=ShiftID)
                ShiftObject.delete()
                page, context = ReturnPageAndContext(request.user)
                return render(request, page, context)
            else:
                print('Remove Shift Not Valid')

        elif 'Lock In Rota' in request.POST:
            print('Lock In Rota Form')
            try:
                FilteredShifts = Shifts.objects.all().filter(Active=True)
                LastShift = FilteredShifts.order_by('Start').last()
                if datetime.today() > LastShift.Start:
                    FilteredShifts.delete()
                    FilteredShifts = Shifts.objects.all().filter(Active=False)
                    for i in FilteredShifts:
                        i.Active = True
                        i.save()
            except:
                print('No Active Schedule')
                FilteredShifts = Shifts.objects.all().filter(Active=False)
                for i in FilteredShifts:
                    i.Active = True
                    i.save()
            page, context = ReturnPageAndContext(request.user)
            return render(request, page, context)

        elif 'Generate Rota' in request.POST:
            print('Generate Rota Form')
            getSchedule()

        elif 'Set Availability' in request.POST:
            print('Set Availability Form')
            SetAvailabilityInstance = SetAvailability(request.POST)
            if SetAvailabilityInstance.is_valid():
                ShiftID = SetAvailabilityInstance['ShiftID'].data[0]
                print(ShiftID)
                UserObject = User.objects.get(username = request.user.username)
                FilteredShifts = Shifts.objects.all().filter(Active=False)
                ShiftObject = FilteredShifts.get(pk=ShiftID)
                EmployeeObject = Employees.objects.get(user=UserObject)
                EmployeeObject.Availability.add(ShiftObject)
            page, context = ReturnPageAndContext(request.user)
            return render(request, page, context)

        elif 'Cancel Availability' in request.POST:
            #print('before')
            #UserName = request.user.username
            #print(UserName)
            CancelAvailabilityInstance = CancelAvailability(request.POST, user=request.user)
            #print('after')
            if CancelAvailabilityInstance.is_valid():
                ShiftToCancel = CancelAvailabilityInstance['ShiftID'].data[0]
                print(ShiftToCancel)
                if ShiftToCancel:
                    Employees.objects.get(user=request.user).Availability.get(pk=ShiftToCancel).delete()

            page, context = ReturnPageAndContext(request.user)
            return render(request, page, context)



        page, context = ReturnPageAndContext(request.user)
        return render(request, page, context)

    #coverRequest = ShiftCoverRequest(user=request.user)
    page, context = ReturnPageAndContext(request.user)
    return render(request, page, context)


def loginsuccess(request):
    context = None
    return render(request, './registration/loginsuccess.html', context)


@login_required(login_url='login')
def rota(request):
    #EmployeeData = Employees.objects.get(user=request.user)
    #if EmployeeData.isManager:
    #    page = './Schedule/rota.html'
    #    context = {}
    #else:

    MonthShiftList, TableHeaders = CreateMonthShiftList()

    context = {
                    'Week1List': MonthShiftList[0],'Week2List': MonthShiftList[1],'Week3List': MonthShiftList[2],
                    'Week4List': MonthShiftList[3],'Week5List': MonthShiftList[4],
                    'Week1TableHeaders': TableHeaders[0], 'Week2TableHeaders': TableHeaders[1],
                    'Week3TableHeaders': TableHeaders[2], 'Week4TableHeaders': TableHeaders[3],
                    'Week5TableHeaders': TableHeaders[4]
                   }
    page = './Schedule/rota.html'
    return render(request, page, context)


@login_required(login_url='login')
def provisionalrota(request):

    MonthShiftList, TableHeaders = CreateProvisionalMonthShiftList()

    context = { 'Week1List': MonthShiftList[0],'Week2List': MonthShiftList[1],'Week3List': MonthShiftList[2],
                'Week4List': MonthShiftList[3],'Week5List': MonthShiftList[4],
                'Week1TableHeaders': TableHeaders[0], 'Week2TableHeaders': TableHeaders[1],
                'Week3TableHeaders': TableHeaders[2], 'Week4TableHeaders': TableHeaders[3],
                'Week5TableHeaders': TableHeaders[4]
                }
    page = './Schedule/provisionalrota.html'

    return render(request, page, context)