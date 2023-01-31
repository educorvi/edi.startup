# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.startup -t test_position.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.startup.testing.EDI_STARTUP_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/startup/tests/robot/test_position.robot
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

Scenario: As a site administrator I can add a Position
  Given a logged-in site administrator
    and an add Invoice form
   When I type 'My Position' into the title field
    and I submit the form
   Then a Position with the title 'My Position' has been created

Scenario: As a site administrator I can view a Position
  Given a logged-in site administrator
    and a Position 'My Position'
   When I go to the Position view
   Then I can see the Position title 'My Position'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Invoice form
  Go To  ${PLONE_URL}/++add++Invoice

a Position 'My Position'
  Create content  type=Invoice  id=my-position  title=My Position

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Position view
  Go To  ${PLONE_URL}/my-position
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Position with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Position title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
