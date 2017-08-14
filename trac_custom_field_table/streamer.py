# Copyright (c) 2017 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

import re

from genshi.builder import tag
from genshi.filters import Transformer
from trac.core import Component, implements
from trac.ticket import Ticket, TicketSystem, ResourceNotFound
from trac.web import ITemplateStreamFilter


OPTIONS_TABLE_KEY = "trac_custom_field_table"
TICKET_FILENAME = "ticket.html"


class TracCustomFieldTable(Component):

    implements(ITemplateStreamFilter)

    # ITemplateStreamFilter methods
    def filter_stream(self, req, method, filename, stream, data):

        """
        1. TODO: style it better
        2. TODO: make an admin panel for it (?)
        3. TODO: show invalid ticket ids, don't just ignore them.
        """

        self.req = req

        if filename == TICKET_FILENAME:
            self.ticket_system = TicketSystemApi(self.env)
            ticket = data.get("ticket")
            stream = self._add_custom_field_tables(stream, ticket)

        return stream

    def _get_table_fields(self, ticket):
        static_headers = ["Ticket"]

        for key, value in self.config.options(OPTIONS_TABLE_KEY):

            if value == "enabled":
                field_value = ticket.values.get(key, "")
                tickets = []
                for ticket_id in field_value.split(","):
                    import pdb
                    pdb.set_trace()
                    ticket_id = re.sub("[^0-9]", "", ticket_id)
                    try:
                        ticket = Ticket(self.env, ticket_id)
                    except ResourceNotFound:
                        continue

                    tickets.append(ticket)

                if tickets:
                    title = self.ticket_system.get_custom_field_label(key)
                    columns_string = self.config.get(
                        OPTIONS_TABLE_KEY,
                        "{}.columns".format(key),
                    )
                    columns = columns_string.strip().split(",")
                    headers = static_headers + columns

                    yield {
                        "key": key,
                        "tickets": tickets,
                        "title": title,
                        "columns": columns,
                        "headers": headers,
                    }

    def _add_custom_field_tables(self, stream, ticket):
        ticket_body = Transformer('//div[@id="ticket"]')

        for table_info in self._get_table_fields(ticket):
            headers = table_info["headers"]
            columns = table_info["columns"]
            tickets = table_info["tickets"]

            table = tag.div(
                tag.h3(table_info["title"]),
                tag.table(
                    tag.thead(self._get_header(headers)),
                    tag.tbody(self._get_body(tickets, columns)),
                    class_="listing tickets",
                ),
            )
            stream = stream | ticket_body.after(table)

        return stream

    def _get_header(self, headers):
        return tag.tr(
            [tag.td(h.title()) for h in headers],
        )

    def _get_body(self, tickets, columns):
        return [
            self._get_row(ticket, columns)
            for ticket in tickets
        ]

    def _get_row(self, ticket, columns):
        cells = []
        for column in columns:
            label = ticket.values.get(column)
            td = tag.td(label, class_=column)
            cells.append(td)

        ticket_class = ""
        ticket_status = ticket.values.get("status")
        if ticket_status == "closed":
            ticket_class = "closed"

        ticket_number = "#{}".format(ticket.id)
        link_td = tag.td(
            tag.a(
                ticket_number,
                class_=ticket_class,
                href=self.req.href.ticket(ticket.id),
                title=ticket_number,
            ),
            class_="id",
        )
        return tag.tr(
            link_td,
            cells,
            class_="trac-columns",
        )


class TicketSystemApi(object):
    """Manages interaction with Trac ticket system"""

    def __init__(self, env):
        self.ticket_system = TicketSystem(env)
        self.custom_fields = self.ticket_system.get_custom_fields()

    def get_custom_field_label(self, custom_field_name):
        """For the given custom field name, get the corresponding label."""

        for custom_field in self.custom_fields:
            if custom_field["name"] == custom_field_name:
                return custom_field["label"]
