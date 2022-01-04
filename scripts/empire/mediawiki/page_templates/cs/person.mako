= ${person.database_identifier} =

{| class="infobox vcard" style="width: 300px; font-size: 95%; text-align: left; border-collapse: collapse;background-color:#e9f2da;" cellpadding="6"
|-
| '''Národnost / Nationality:'''
| ${person.nationality if person.nationality else ''}
|-
| '''Rok narození / Year of birth:'''
| ${to_s(year_of_birth)}
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

% if len(other_relationships) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Právnická nebo fyzická osoba ve vztahu / Related legal entity or person
! style="text-align:left;" | Od / Since date
! style="text-align:left;" | Do / Until date
! style="text-align:left;" | Poznámky / Details
% for other_relationship in other_relationships:
|-
| style="text-align:left;" | [[${other_relationship.legal_entity.database_identifier}]]
| style="text-align:left;" | ${to_s(other_relationship.related_since_date)}
| style="text-align:left;" | ${to_s(other_relationship.related_until_date)}
| style="text-align:left;" | ${to_s(other_relationship.relationship_details)}
% endfor
|}
% endif
% if len(other_relationships) == 0:
''Nemá další vztahy / No other relationships''
% endif

== Další poznámky / Other notes ==

${person.other_notes if person.other_notes else "''Žádné další poznámky / No other notes''"}

== Zdroje / Sources ==

% if len(sources) > 0:
% for source in sources:
* ${"''" + source.summary + "'' " if source.summary is not None else ''}${source.url + ' ' if source.url is not None else ''}${'(Naposledy kontrolováno / Last checked: ' + source.last_checked_date.strftime('%Y-%m-%d') + ')' if source.last_checked_date is not None else ''}
% endfor
% endif
% if len(sources) == 0:
''Bez zdrojů / No sources''
% endif

[[Kategorie:Fyzické osoby / People]]
