import datetime
from html import escape as escape_html

from pony.orm import *
from database import db


class Believer(db.Entity):
    phone_nr = Optional(str)
    account_nr = Optional(str)
    bank_name = Optional(str)
    remark = Optional(str)
    attached_file = Optional(str)
    reported_by = Set("Reporter")
    added_by = Required("Admin")
    created = Required(datetime.datetime, default=datetime.datetime.now)

    def __str__(self):
        reported_count = len(self.reported_by)
        reported_list = ', '.join(
            [str(reporter) for reporter in self.reported_by][:3]) + (
                ' and %d others' % (reported_count - 3)
                if reported_count > 3
                else '')

        params = {
            'id': self.id,
            'phone_nr': self.phone_nr,
            'account_nr': self.account_nr,
            'bank_name': self.bank_name,
            'remark': self.remark,
            'reported_by': reported_list,
            'added_by': self.added_by
        }

        s = ("<b>Distributor #{id}</b>\n"
             "_____________________\n"
             "<b>[</b>{account_nr}<b>]</b>\n"
             "Updated: {phone_nr}\n"
             "Dealership:\n {bank_name}\n"
             "<b>==></b> {remark}\n"
             "Voted by: {reported_by}\n"
             "Owner: {added_by}").format(
                **{k: escape_html(str(v)) for (k, v) in params.items()}
            )

        print(s)

        return s

    def __repr__(self):
        return str(self)
