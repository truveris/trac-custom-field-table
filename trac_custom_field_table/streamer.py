# Copyright (c) 2017 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

from genshi.builder import tag
from genshi.filters import Transformer
from trac.core import Component, implements
from trac.ticket import Ticket
from trac.web import ITemplateStreamFilter


class TracCustomFieldTable(Component):

    implements(ITemplateStreamFilter)

    # ITemplateStreamFilter methods
    def filter_stream(self, req, method, filename, stream, data):

        """
        1. TODO: turn this into functions
        2. TODO: get display columns from config
        3. TODO: style it better
        4. TODO: using the config option custom field column name, fetch all
        custom fields and with that, get the display name of the custom field,
        and use that as the header.

        """

        columns = ["Summary", "Milestone", "Owner"]
        headers = ["Ticket"] + columns

        if filename == 'ticket.html':

            ticket_body = Transformer('//div[@id="ticket"]')
            for key, value in self.config.options("trac_custom_field_table"):

                if value == "enabled":
                    # Get the ticket info.
                    ticket = data.get('ticket')
                    field_value = ticket.values.get(key, "").strip()
                    if field_value:
                        ticket_ids = field_value.split(",")

                        # TODO: create this imperitively
                        tablediv = tag.div(
                            tag.h3("Dependencies"),
                        )
                        table = tag.table(class_="listing tickets")
                        header_tds = [tag.td(h) for h in headers]
                        thead = tag.thead()
                        thead.append(tag.tr(header_tds))

                        trs = []

                        for ticket_id in ticket_ids:
                            tr = tag.tr(class_="trac-columns")
                            tr.append(tag.td(ticket_id))
                            trs.append(tr)

                            # TODO: make ticket id a link
                            ticket = Ticket(self.env, ticket_id)
                            for column in columns:
                                lowercase = column.lower()
                                td = tag.td(
                                    ticket.values.get(lowercase),
                                    class_=lowercase,
                                )
                                tr.append(td)

                        tbody = tag.tbody()

                        for tr in trs:
                            tbody.append(tr)

                        table.append(thead)
                        table.append(tbody)
                        tablediv.append(table)
                        stream = stream | ticket_body.after(tablediv)

        return stream
