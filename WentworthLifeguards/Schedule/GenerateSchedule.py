from .models import Employees, Shifts
from django.contrib.auth.models import User


Shifts = Shifts.objects.all().filter(Active=False)


def getEmployeeAvailability():
    '''
    The function returns a list of lists, that are structured so that:
    [[Employee -(Object)-, Shifts Available To Work (List of shift object primary keys), Number of Shifts Available (Integer)]]
    '''

    #OrderedEmployees = Employees.objects.order_by('user__first_name')
    EmployeeAvailability = []
    for Employee in Employees.objects.all():
        EmployeeUsername =Employee.user.username
        Availability = []
        NumOfShifts = 0
        for Shift in Employee.Availability.all():
            Availability.append(Shift.pk)
            NumOfShifts += 1
        EmployeeAvailability.append([EmployeeUsername, Availability, NumOfShifts])

    EmployeeAvailability = sorted(EmployeeAvailability, key=lambda x: x[2])

    return EmployeeAvailability


def clearLockedShifts():
    from .models import Shifts
    for i in Shifts.objects.all().filter(Active=True):
        i.delete()


def assignShifts(EmployeeAvailability):

    while EmployeeAvailability:
        Employee = EmployeeAvailability.pop(0)
        NumOfShifts = Employee[2]
        if NumOfShifts > 0:
            Shift = Shifts.get(pk=Employee[1][0])
            UserObject = User.objects.get(username=Employee[0])
            EmployeeObject = Employees.objects.get(user=UserObject)
            if Shift.Employees == None:
                Shift(Employees=EmployeeObject)
                Shift.save()
            if NumOfShifts > 1:
                NumOfShifts -= 1
                Employee[2] = NumOfShifts
                del Employee[1][0]
                EmployeeAvailability.append(Employee)
                print('EmployeeFullyScheduled')
            print('ShiftFilled')


def getSchedule():
    EmployeeAvailability = getEmployeeAvailability()
    assignShifts(EmployeeAvailability)


