# Zero Hour COntract Scheduling

https://www.aidengourley.com/static/mainPage/other/CasualContractSchedulingDevelopmentProcessDocumentation.pdf

A very common time-consuming exercise for management, particularly within corporations that operate shift-based working hours, is the scheduling that takes place, usually by hand. 
The purpose of this web application is to reduce the time management spend on this task, while ensuring reference and changes can be accommodated for each stakeholder. The manager will build the timetable they require and publish the shifts they require to be filled. Each employee will have an individual account with which they are able to choose shifts they would like to be selected for. The manager has an option to choose when to run the scheduler and commit the changes to the following month's schedule.

(This project was based on a real case study; however the organisation has not implemented the software. All rights to the contents of this repository remain with Aiden Gourley. No content can be copied, changed, or redistributed.)

						||!!|| The Scheduling Algorithm ||!!||

The objective of the algorithm is to ensure a full schedule, and where there are conflicts between two employees regarding shifts, provide a fair solution based on the number of shifts assigned to each employee that month.
The pseudocode is as follows:

	[ASSUME pop(), append(), get(), (Database items are accessed as objects)]

	PROCEDURE GetSchedule()
		EmployeeAvailability ← CALL GetEmployeeAvailability
		CALL AssignShifts(EmployeeAvailability) 
	END PROCEDURE 
	
	FUNCTION GetEmployeeAvailability()
		EmployeeAvailability ← [ ]
		FOR Employee IN Employees DO
			EmployeeUsername ← Employee.user.username
			Availability ← [ ]
			NumberOfShifts ← 0
			FOR Shift IN Employee.Availability.all() DO
					Availability.Append(Shift.pk)
					NumberOfShifts ← NumberOfShifts + 1
			END FOR
			AvailabiityList ← [EmployeeUsername, Availability, NumberOfShifts]
			EmployeeAvailability.append(AvailabilityList)
		END FOR
		EmployeeAvailability ← ResverseSort(EmployeeAvailability[2])
		RETURN EmployeeAvailability
	END FUNCTION

	PROCEDURE AssignShifts(EmployeeAvailability)
		WHILE EmployeeAvailability NOT Null DO
			Employee ← EmployeeAvailability.pop(0)
			NumberOfShifts ← Employee[2]
			IF NumberOfShifts > 0 THEN
				Shift ← Shifts.get(pk=Employee[1][0])
				EmployeeObject ← Employees.objects.get(username=Employee[0])
				IF Shift.Employees = None THEN
					Shift(Employees=EmployeeObject)
				END IF
				IF NumOfShifts > 1 THEN
					NumberOfShifts = NumberOfShifts - 1
					Employee[2] ← NumberOfShifts
					Employee[1][0].delete()
					EmployeeAvailability.append(Employee)
				END IF
			END IF
		END WHILE
	END PROCEDURE

