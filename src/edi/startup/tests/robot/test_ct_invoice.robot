# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.startup -t test_invoice.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.startup.testing.EDI_STARTUP_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/startup/tests/robot/test_invoice.robot
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

Scenario: As a site administrator I can add a Invoice
  Given a logged-in site administrator
    and an add Invoice form
   When I type 'My Invoice' into the title field
    and I submit the form
   Then a Invoice with the title 'My Invoice' has been created

Scenario: As a site administrator I can view a Invoice
  Given a logged-in site administrator
    and a Invoice 'My Invoice'
   When I go to the Invoice view
   Then I can see the Invoice title 'My Invoice'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Invoice form
  Go To  ${PLONE_URL}/++add++Invoice

a Invoice 'My Invoice'
  Create content  type=Invoice  id=my-invoice  title=My Invoice

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Invoice view
  Go To  ${PLONE_URL}/my-invoice
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Invoice with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Invoice title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
