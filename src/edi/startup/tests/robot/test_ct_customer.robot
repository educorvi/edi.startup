# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.startup -t test_customer.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.startup.testing.EDI_STARTUP_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/startup/tests/robot/test_customer.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Customer
  Given a logged-in site administrator
    and an add Customer form
   When I type 'My Customer' into the title field
    and I submit the form
   Then a Customer with the title 'My Customer' has been created

Scenario: As a site administrator I can view a Customer
  Given a logged-in site administrator
    and a Customer 'My Customer'
   When I go to the Customer view
   Then I can see the Customer title 'My Customer'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Customer form
  Go To  ${PLONE_URL}/++add++Customer

a Customer 'My Customer'
  Create content  type=Customer  id=my-customer  title=My Customer

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Customer view
  Go To  ${PLONE_URL}/my-customer
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Customer with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Customer title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
