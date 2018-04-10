from test_plus.test import TestCase
from django.contrib.auth.models import Group


from ..models import Employee


class TestModelEmployee(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.employee = Employee.objects.create(
            cpf="974.220.200-16",
            user=self.user,
            departament=Employee.NEUROLOGY
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/users/testuser/'
        )

    def test_one_to_one_relation(self):
        self.assertIs(self.user, self.employee.user)
        self.assertIs(self.employee, self.user.employee)

    def test_delete_cascade(self):

        self.assertEquals(
            Employee.objects.get(cpf="974.220.200-16"),
            self.employee
        )

        self.user.delete()

        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(cpf="974.220.200-16")

    def test__str__(self):
        self.assertEqual(
            self.employee.__str__(),
            (
                self.user.get_username() +
                " - " +
                self.employee.get_departament_display()
            )
        )


class TestModelEmployeeNoSetUp(TestCase):

    def test_save_making_changes_on_user(self):

        # this test should have no setup executed before it

        self.user = self.make_user()

        self.assertEquals(self.user.is_staff, False)

        with self.assertRaises(Group.DoesNotExist):
            self.user.groups.get(name=Employee.GROUP_NAME)

        # now we add the employee<--->user relation
        self.employee = Employee.objects.create(
            cpf="974.220.200-16",
            user=self.user,
            departament=Employee.NEUROLOGY
        )

        # it should create the group
        employee_group = Group.objects.get(name=Employee.GROUP_NAME)

        # and change things in the user
        self.assertEquals(self.user.is_staff, True)
        self.assertEqual(
            self.user.groups.get(name=Employee.GROUP_NAME),
            employee_group
        )
