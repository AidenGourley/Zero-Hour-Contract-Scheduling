from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Shifts, Employees
from datetime import datetime
from calendar import monthrange


############SHIFT COVER REQUESTS################

def PopulateShiftCoverRequestMenus(user):

    UserShiftList = [(None, 'None')]

    #GET USER'S SHIFTS#
    UserShifts = Shifts.objects.filter(Employees=Employees.objects.get(user=user))
    for i in UserShifts:
        ShiftDate = i.Start.strftime('%b %d')
        ShiftStartTime = i.Start.strftime('%H:%M')
        ShiftEndTime = i.End.strftime('%H:%M')
        ShiftString = ShiftDate + ' | ' + ShiftStartTime + ' - ' + ShiftEndTime
        UserShiftList.append((i, ShiftString))


    #print(UserShiftList)#
    return UserShiftList#, other_employees


class ShiftCoverRequest(forms.Form):
    def __init__(self, user):
        super(ShiftCoverRequest, self).__init__()
        Choices= PopulateShiftCoverRequestMenus(user)
        self.fields['UserShift'] = forms.ChoiceField(label="Choose Shift To Request Cover For ", choices=Choices)

################################################

############USER REGISTRATION###################

class UserRegistrationPart1(UserCreationForm, forms.Form):
    #Make Pre-built Django UserCreationForm Fields Mandatory
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2')


    def save(self, commit=True):
        user = super(UserRegistrationPart1, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserRegistrationPart2(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ('isManager',
                  'PhoneNo')


class RemoveUser(forms.Form):

    def __init__(self,user):
        super(RemoveUser, self).__init__()
        ChoicesList = []
        ExcludedOptions = ['root']
        for i in User.objects.filter(employees__isManager=True):
            ExcludedOptions.append(i.username)
        for i in User.objects.all().exclude(username__in=ExcludedOptions):
            string = str(i.first_name + ' ' + i.last_name)
            username = i.username
            ChoicesList.append((username, string))
        Choices = tuple(ChoicesList)

        self.fields['username'] = forms.ChoiceField(label="Delete User ", choices=Choices)

################################################

############SHIFT ADDITION AND REMOVAL##########


class AddShifts(forms.Form):
    CurrentYear = int(datetime.now().year)
    CurrentMonth = int(datetime.now().month)
    DAYS = []
    for i in range(1, 32):
        DAYS.append((i, str(i)))
    DAYS = tuple(DAYS)
    MaxMonthValue = CurrentMonth+1
    if MaxMonthValue == 13:
        MaxMonthValue = 1

    StartTime = forms.TimeField(widget=forms.TimeInput(), label='Start Time:', required=True)
    EndTime = forms.TimeField(widget=forms.TimeInput(), label='End Time ', required=True)
    Month = forms.IntegerField(max_value=MaxMonthValue, min_value=CurrentMonth, initial=MaxMonthValue)
    Year = forms.IntegerField(max_value=CurrentYear + 1, min_value=CurrentYear, initial=CurrentYear)
    Days = forms.MultipleChoiceField(choices=DAYS)


    def clean_Days(self):
        SelectedMonth = self.cleaned_data['Month']
        SelectedYear = self.cleaned_data['Year']
        DaysInMonth = monthrange(SelectedYear, SelectedMonth)[1]
        for i in self.cleaned_data['Days']:
            if int(i) > int(DaysInMonth):
                raise forms.ValidationError('You selected more days than are in the month.')
        return self.cleaned_data['Days']


def GetShifts(SetActive):
    ChoicesList = []
    for i in Shifts.objects.all().filter(Active=SetActive):
        String = str(i.Start.strftime('%d/%m/%Y %H:%M') + ' - ' + i.End.strftime('%d/%m/%Y %H:%M'))
        ShiftID = i.pk
        ChoicesList.append((ShiftID, String))
    Choices = tuple(ChoicesList)
    return Choices


class RemoveShift(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RemoveShift, self).__init__(*args, **kwargs)
        Choices = GetShifts(SetActive=False)
        self.fields['ShiftID'] = forms.ChoiceField(label='Delete Shift ', choices=Choices)

##############Employee Availability############

def getUserAvailability(user):
    #user = User.objects.get(username=username)
    EmployeeObject = Employees.objects.get(user=user)
    Availability = EmployeeObject.Availability.all().filter(Active=False)

    #FilteredShifts = Shifts.objects.all().filter(Active=False)
    #Availability = FilteredShifts.filter(Employees=EmployeeObject)
    print('lol'+str(Availability))
    ChoicesList = []
    for Shift in Availability:
        String = str(Shift.Start.strftime('%d/%m/%Y %H:%M') + ' - ' + Shift.End.strftime('%d/%m/%Y %H:%M'))
        ShiftID = Shift.pk
        print(ShiftID)
        ChoicesList.append((ShiftID, String))
    Choices = tuple(ChoicesList)
    return Choices



class SetAvailability(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SetAvailability, self).__init__(*args, **kwargs)
        Choices = GetShifts(SetActive=False)
        self.fields['ShiftID'] = forms.MultipleChoiceField(label='', choices=Choices)


class CancelAvailability(forms.Form):
    def __init__(self, *args, user, **kwargs):
        super(CancelAvailability, self).__init__(*args, **kwargs)
        Choices = getUserAvailability(user)
        self.fields['ShiftID'] = forms.MultipleChoiceField(label='', choices=Choices)

