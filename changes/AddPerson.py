from PLC.Faults import *
from PLC.Method import Method
from PLC.Parameter import Parameter, Mixed
from PLC.Persons import Person, Persons
from PLC.Auth import Auth
import uuid ##################################soners

can_update = lambda (field, value): field in \
             ['first_name', 'last_name', 'title',
              'email', 'password', 'phone', 'url', 'bio']

class AddPerson(Method):
    """
    Adds a new account. Any fields specified in person_fields are
    used, otherwise defaults are used.

    Accounts are disabled by default. To enable an account, use
    UpdatePerson().

    Returns the new person_id (> 0) if successful, faults otherwise.
    """

    roles = ['admin', 'pi']

    person_fields = dict(filter(can_update, Person.fields.items()))

    accepts = [
        Auth(),
        person_fields
        ]

    returns = Parameter(int, 'New person_id (> 0) if successful')

    def call(self, auth, person_fields):
        person_fields = dict(filter(can_update, person_fields.items()))
	person_fields['uuid'] = str(uuid.uuid4().int)###############################soners
        person_fields['enabled'] = False
        person = Person(self.api, person_fields)
        person.sync()

	# Logging variables
	self.event_objects = {'Person': [person['person_id']]}
	self.message = 'Person %d added' % person['person_id']	

        return person['person_id']
