= ${legal_entity.database_identifier} =

{| class="infobox vcard" style="width: 300px; font-size: 95%; text-align: left; border-collapse: collapse;background-color:#e9f2da;" cellpadding="6"
|-
| '''Typ právnické osoby / Legal entity type:'''
| ${to_s(legal_entity.legal_entity_type)}
|-
| '''Identifikátor (IČO, ...) / Identification number:'''
| ${to_s(legal_entity.identification_number)}
|-
| '''Adresa / Address:'''
| ${to_s(legal_entity.address)}
|-
| '''Země / Country:'''
| ${to_s(legal_entity.country)}
|-
| '''Datum založení / Foundation date:'''
| ${to_s(legal_entity.foundation_date)}
|-
| '''Datum zániku / Dissolution date:'''
| ${to_s(legal_entity.dissolution_date)}
|-
|}

== Majitelé / Owners ==

% if len(owners) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Majitel / Owner
! style="text-align:left;" | Vlastněná procenta / Owned percentage
! style="text-align:left;" | Majitelem od / Owned since date
! style="text-align:left;" | Majitelem do / Owned until date
! style="text-align:left;" | Poznámky / Details
% for owner in owners:
|-
% if owner['owner_legal_entity_or_person']:
| style="text-align:left;" | [[${owner['owner_legal_entity_or_person'].database_identifier}]]
% else:
| style="text-align:left;" | ${owner['info_line']}
(''Majitel není v databázi / Owner not in the database'')
% endif
| style="text-align:left;" | ${to_s(owner['owned_percentage'])}
| style="text-align:left;" | ${to_s(owner['owned_since_date'])}
| style="text-align:left;" | ${to_s(owner['owned_until_date'])}
| style="text-align:left;" | ${to_s(owner['ownership_details'])}
% endfor
|}
% endif
% if len(owners) == 0:
''Majitelé chybí / Missing owners''
% endif

== Je majitelem / Is owner of  ==

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
% if other_relationship['related_legal_entity_or_person']:
| style="text-align:left;" | [[${other_relationship['related_legal_entity_or_person'].database_identifier}]]
% else:
| style="text-align:left;" | ${other_relationship['info_line']}
(''Není v databázi / Not in the database'')
% endif
| style="text-align:left;" | ${to_s(other_relationship['related_since_date'])}
| style="text-align:left;" | ${to_s(other_relationship['related_until_date'])}
| style="text-align:left;" | ${to_s(other_relationship['relationship_details'])}
% endfor
|}
% endif
% if len(other_relationships) == 0:
''Nemá další vztahy / No other relationships''
% endif

== Dotace / Subsidies ==

* Počet dotací / Subsidies count: ${subsidies_count}
* Celková částka [EUR] / Total amount [EUR]: ${format_amount(subsidies_sum)}
% if len(subsidies) > 0:

{| class="wikitable sortable"
|-
! style="text-align:left;" | Identifikátor / Identifier
! style="text-align:left;" | Rok / Year
! style="text-align:left;" | Název projektu / Project name
! style="text-align:right;" data-sort-type="number" | Celková částka dotace [EUR] / Subsidy total amount [EUR]
% for subsidy in subsidies:
|-
| style="text-align:left;" | [[${subsidy['database_identifier']}]]
| style="text-align:left;" | ${to_s(subsidy['year'])}
| style="text-align:left;" | ${to_s(subsidy['project_name'])}
| style="text-align:right;" data-sort-value="${subsidy['total_amount_in_eur']}" | ${format_amount(subsidy['total_amount_in_eur'])}
% endfor
|}
% endif

== Předchozí názvy / Previous names ==

% if len(previous_names) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Předchozí název / Previous name
! style="text-align:left;" | Od / Since date
! style="text-align:left;" | Do / Until date
% for previous_name in previous_names:
|-
| style="text-align:left;" | ${to_s(previous_name.previous_name)}
| style="text-align:left;" | ${to_s(previous_name.named_since_date)}
| style="text-align:left;" | ${to_s(previous_name.named_until_date)}
% endfor
|}
% endif
% if len(previous_names) == 0:
''Nemá předchozí názvy / No previous names''
% endif

== Předchozí adresy / Previous addresses ==

% if len(previous_addresses) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Předchozí adresa / Previous address
! style="text-align:left;" | Od / Since date
! style="text-align:left;" | Do / Until date
% for previous_address in previous_addresses:
|-
| style="text-align:left;" | ${to_s(previous_address.previous_address)}
| style="text-align:left;" | ${to_s(previous_address.address_since_date)}
| style="text-align:left;" | ${to_s(previous_address.address_until_date)}
% endfor
|}
% endif
% if len(previous_addresses) == 0:
''Nemá předchozí adresy / No previous addresses''
% endif

== Zmínky v médiích / Media mentions ==

% if len(media_mentions) > 0:
% for media_mention in media_mentions:
* ${media_mention.summary + ' ' if media_mention.summary else ''}[${media_mention.url} ${media_mention.url}]${' Naposledy kontrolováno / Last checked: ' + media_mention.last_checked_date if media_mention.last_checked_date else ''}
% endfor
% endif
% if len(media_mentions) == 0:
''Nemá zmínky v médiích / No media mentions''
% endif

== Další poznámky / Other notes ==

${legal_entity.other_notes if legal_entity.other_notes else "''Žádné další poznámky / No other notes''"}

== Zdroje / Sources ==

% if len(sources) > 0:
% for source in sources:
* ${"''" + source.summary + "'' " if source.summary is not None else ''}${source.url + ' ' if source.url is not None else ''}${'(Naposledy kontrolováno / Last checked: ' + source.last_checked_date.strftime('%Y-%m-%d') + ')' if source.last_checked_date is not None else ''}
% endfor
% endif
% if len(sources) == 0:
''Bez zdrojů / No sources''
% endif

[[Kategorie:Právnické osoby / Legal entities]]
% if legal_entity.legal_entity_type is not None:
[[Kategorie:Typ právnické osoby ${legal_entity.legal_entity_type} / Legal entity type ${legal_entity.legal_entity_type}]]
% endif
