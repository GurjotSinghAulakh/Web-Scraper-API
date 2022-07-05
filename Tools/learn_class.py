class Employee:
    raise_amount = 1.04

    def __init__(self, firstname, lastname, pay):
        self.firstname = firstname
        self.lastname = lastname
        self.pay = pay
        self.email = firstname + "." + lastname + "@email.com"

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    def fullname(self):
        return "{} {}".format(self.firstname, self.lastname)


class Developer(Employee):
    def __init__(self, firstname, lastname, pay, prog_lang):
        super().__init__(firstname,lastname, pay)
        self.prog_lang = prog_lang


class Manager(Employee):
    def __init__(self, firstname, lastname, pay, employees=None): # when a mananger first starts they have no employees
        super().__init__(firstname, lastname, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def add_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emp(self):
        for emp in self.employees:
            print(emp.fullname())


dev_1 = Developer("Cory", "Jokan", 50000, "Python")


mgr_1 = Manager("Sue", "Smith", 90000, [dev_1])

print(mgr_1.email)
print(mgr_1.print_emp())
