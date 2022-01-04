= ${person.database_identifier} =

{| class="infobox vcard" style="width: 300px; font-size: 95%; text-align: left; border-collapse: collapse;background-color:#e9f2da;" cellpadding="6"
|-
| '''Nationality:'''
| ${person.nationality if person.nationality else ''}
|-
| '''Year of birth:'''
| ${to_s(year_of_birth)}
|-
| '''Residence country:'''
| ${person.residence_country if person.residence_country else ''}
|-
| '''Residence city:'''
| ${person.residence_city if person.residence_city else ''}
|}

== Is owner of ==

% if len(owning) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Owned legal entity
! style="text-align:left;" | Owned percentage
! style="text-align:left;" | Owned since date
! style="text-align:left;" | Owned until date
! style="text-align:left;" | Details
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
''Is not owning any legal entities''
% endif

== Other relationships ==

% if len(other_relationships) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Related legal entity or person
! style="text-align:left;" | Since date
! style="text-align:left;" | Until date
! style="text-align:left;" | Details
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
''No other relationships''
% endif

== Other notes ==

${person.other_notes if person.other_notes else "''No other notes''"}

== Zdroje / Sources ==

% if len(sources) > 0:
% for source in sources:
* ${"''" + source.summary + "'' " if source.summary is not None else ''}${source.url + ' ' if source.url is not None else ''}${'(Last checked: ' + source.last_checked_date.strftime('%Y-%m-%d') + ')' if source.last_checked_date is not None else ''}
% endfor
% endif
% if len(sources) == 0:
''No sources''
% endif

[[Category:People]]
