# -*- coding: utf-8 -*-
import json
from datetime import datetime
from edi.startup import _
from Products.Five.browser import BrowserView
from plone import api
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from z3c.relationfield import RelationValue

class ImportView(BrowserView):

    def __call__(self):
        self.validateview = self.context.absolute_url() + "/@@validate-view"
        return self.index()

class ValidateView(BrowserView):

    def __call__(self):
        self.intids = getUtility(IIntIds)
        url = self.context.absolute_url() + "/@@import-view"
        jsondata = self.request.form.get('jsondata')
        if not jsondata:
            message = _('Please insert JSON-Data in Textfield and click the "Check and Import Button"')
            api.portal.show_message(message=message, request=self.request, type='error')
            return self.request.response.redirect(url)
        try:
            clickerdata = json.loads(jsondata)
        except:
            message = _("The inserted data does not have a json format")
            api.portal.show_message(message=message, request=self.request, type='error')
            return self.request.response.redirect(url)
        invoicedict = self.create_invoice_dict(clickerdata)
        invoices = self.create_invoice_objects(invoicedict)
        message = _("The invoices were successfully created")
        api.portal.show_message(message=message, request=self.request, type='success')
        url = self.context.absolute_url()
        return self.request.response.redirect(url)

    def create_invoice_dict(self, clickerdata):
        """
          create Invoices form clickerdata
          {
            "id": "7885b030-387a-41d6-a564-0e076f35eb9d",
            "from": "2022-12-14T14:06:00.000Z",
            "to": "2022-12-14T17:00:00.000Z",
            "note": "",
            "private_note": "",
            "task": {
                "id": "75be0fb2bdd445398832154777186320",
                "title": "Indexierung aller relvanten Daten aus den Objekten der Projektsteuerung",
                "note_mandatory": false,
                "open": true
                },
            "user": {
            "id": "af67dfcd-d110-4159-a362-7b1c9036ab80",
            "email": "julian.pollinger@educorvi.de",
            "name": "Julian Pollinger"
            }
          }
        """
        billfolder = {}
        for element in clickerdata:
            start = datetime.strptime(element["from"][:19], "%Y-%m-%dT%H:%M:%S")
            end = datetime.strptime(element["to"][:19], "%Y-%m-%dT%H:%M:%S")
            delta = end - start
            hours = delta.seconds / 3600
            employee = element["user"]["email"]
            hours = self.calculate_hours_for_employee(employee, hours)
            comment = element["note"]
            task = element["task"]["id"]
            taskobj = api.content.get(UID = task)
            if taskobj.portal_type == 'Todo Task':
                project = taskobj.aq_parent
                tasktitle = taskobj.title
            else:
                project = taskobj
                tasktitle = _("General project work")
            projectuid = project.UID()
            projectvalue = self.intids.getId(project)
            customer = project.customer
            if not customer:
                customer = project.aq_parent.customer
            if not customer:
                continue

            if projectuid not in billfolder:
                billfolder[projectuid] = {}
                billfolder[projectuid]["title"] = project.title
                billfolder[projectuid]["invoice_nr"] = ""
                billfolder[projectuid]["customer"] = customer
                billfolder[projectuid]["project"] = RelationValue(projectvalue)
                billfolder[projectuid]["positions"] = {}
                billfolder[projectuid]["positions"][task] = {"title" : tasktitle,
                                                              "description": comment,
                                                              "start": start,
                                                              "end" : end,
                                                              "hours_practice" : hours["practice"],
                                                              "hours_trainee" : hours["trainee"],
                                                              "hours_professional" : hours["professional"],
                                                              "hours_expert" : hours["expert"]}
            else:
                positions = billfolder[projectuid]["positions"]
                if task not in positions:
                    billfolder[projectuid]["positions"][task] = {"title" : tasktitle,
                                                                  "description": comment,
                                                                  "start": start,
                                                                  "end" : end,
                                                                  "hours_practice" : hours["practice"],
                                                                  "hours_trainee" : hours["trainee"],
                                                                  "hours_professional" : hours["professional"],
                                                                  "hours_expert" : hours["expert"]}
                else:
                    position = billfolder[projectuid]["positions"][task]
                    if comment:
                        position["description"] += (', ' + comment)
                    position["end"] = end
                    position["hours_practice"] += hours["practice"]
                    position["hours_trainee"] += hours["trainee"]
                    position["hours_professional"] += hours["professional"]
                    position["hours_expert"] += hours["expert"]
                    billfolder[projectuid]["positions"][task] = position
        return billfolder

    def calculate_hours_for_employee(self, employee, delta):
        skills = {'practice':0, 'trainee':0, 'professional':0, 'expert':0}
        current_user = None
        users = api.user.get_users()
        for user in users:
            if user.getProperty('email') == employee:
                current_user = user
        if not current_user:
            return skills
        groups = api.group.get_groups(user=current_user)
        groups = [group.id for group in groups]
        if not groups:
            return skills
        hours = round(delta)
        if hours == 0:
            hours = 1
        if 'expert' in groups:
            skills['expert'] += hours
            return skills
        elif 'professional' in groups:
            skills['professional'] += hours
            return skills
        elif 'trainee' in groups:
            skills['trainee'] += hours
            return skills
        elif 'practice' in groups:
            skills['practice'] += hours
            return skills
        return skills

    def create_invoice_objects(self, invoicedict):
        for raw in invoicedict.values():
            invoice = api.content.create(
                type='Invoice',
                title=raw.get('title'),
                customer=raw.get('customer'),
                project=raw.get('project'),
                container=self.context)
            for pos in raw['positions'].values():
                position = api.content.create(
                    type = 'Position',
                    title = pos.get('title'),
                    description = pos.get('description'),
                    start = pos.get('start'),
                    end = pos.get('end'),
                    hours_practice = pos.get('hours_practice'),
                    hours_trainee = pos.get('hours_trainee'),
                    hours_professional = pos.get('hours_professional'),
                    hours_expert = pos.get('hours_expert'),
                    container = invoice)
        return invoice
