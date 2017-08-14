Description
=============
Works with custom fields that are set for tickets. The custom fields must
contain a single, or comma-separated list, of ticket ids. For each "linked"
ticket id in the custom field, this plugin will insert a table at the bottom
of the ticket, showing details about the "linked" ticket(s).

How to set up
=============
In your trac.ini config file, add a new section titled `trac_custom_field_table`
As the keys, use whatever custom field name or names you have defined elsewhere
in the config, under `ticket-custom`.

As the value, use `enabled` to turn on the display of the table within any
ticket that has value(s) inside that custom field. Any other value than
`enabled` will not show the table.

Then, as a sub-item under the same custom field name, list the columns to display
in the report. I.e. `field.columns = summary, owner`

Example
=======
[ticket-custom]
dependencies = text

[trac_custom_field_table]
dependencies = enabled
dependencies.columns = summary, milestone, owner
