= ${person.database_identifier} =

{| class="infobox vcard" style="width: 300px; font-size: 95%; text-align: left; border-collapse: collapse;background-color:#e9f2da;" cellpadding="6"
|-
| '''Národnost / Nationality:'''
| ${person.nationality if person.nationality else ''}
|-
| '''Rok narození / Year of birth:'''
| TODO
|-
| '''Země pobytu / Residence country:'''
| ${person.residence_country if person.residence_country else ''}
|-
| '''Město pobytu / Residence city:'''
| ${person.residence_city if person.residence_city else ''}
|}

== Je majitelem / Is owner of ==

% if len(owning) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Vlastěná právnická osoba / Owned legal entity
! style="text-align:left;" | Vlastněná procenta / Owned percentage
! style="text-align:left;" | Majitelem od / Owned since date
! style="text-align:left;" | Majitelem do / Owned until date
! style="text-align:left;" | Poznámky / Details
% for owner in owning:
|-
| style="text-align:left;" | [[${owner.owned_legal_entity.database_identifier}]]
| style="text-align:left;" | ${to_s(owner.owned_percentage)}
| style="text-align:left;" | ${to_s(owner.owned_since_date)}
| style="text-align:left;" | ${to_s(owner.owned_until_date)}
| style="text-align:left;" | ${to_s(owner.ownership_details)}
% endfor
|}
% endif
% if len(owning) == 0:
''Není majitelem žádné právnické osoby / Is not owning any legal entities''
% endif

== Další vztahy / Other relationships ==

TODO

== Další poznámky / Other notes ==

${person.other_notes if person.other_notes else "''Žádné další poznámky / No other notes''"}

== Zdroje / Sources ==

TODO

[[Kategorie:Fyzické osoby / People]]
