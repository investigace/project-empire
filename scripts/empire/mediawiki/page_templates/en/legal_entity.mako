= ${legal_entity.database_identifier} =

{| class="infobox vcard" style="width: 300px; font-size: 95%; text-align: left; border-collapse: collapse;background-color:#e9f2da;" cellpadding="6"
|-
| '''Legal entity type:'''
| ${to_s(legal_entity.legal_entity_type)}
|-
| '''Identification number:'''
| ${to_s(legal_entity.identification_number)}
|-
| '''Address:'''
| ${to_s(legal_entity.address)}
|-
| '''Country:'''
| ${to_s(legal_entity.country)}
|-
| '''Foundation date:'''
| ${to_s(legal_entity.foundation_date)}
|-
| '''Dissolution date:'''
| ${to_s(legal_entity.dissolution_date)}
|-
|}

== Owners ==

% if len(owners) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Owner
! style="text-align:left;" | Owned percentage
! style="text-align:left;" | Owned since date
! style="text-align:left;" | Owned until date
! style="text-align:left;" | Details
% for owner in owners:
|-
% if owner['owner_legal_entity_or_person']:
| style="text-align:left;" | [[${owner['owner_legal_entity_or_person'].database_identifier}]]
% else:
| style="text-align:left;" | ${owner['info_line']}
(''Owner not in the database'')
% endif
| style="text-align:left;" | ${to_s(owner['owned_percentage'])}
| style="text-align:left;" | ${to_s(owner['owned_since_date'])}
| style="text-align:left;" | ${to_s(owner['owned_until_date'])}
| style="text-align:left;" | ${to_s(owner['ownership_details'])}
% endfor
|}
% endif
% if len(owners) == 0:
''Missing owners''
% endif

== Is owner of  ==

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
% if other_relationship['related_legal_entity_or_person']:
| style="text-align:left;" | [[${other_relationship['related_legal_entity_or_person'].database_identifier}]]
% else:
| style="text-align:left;" | ${other_relationship['info_line']}
(''Not in the database'')
% endif
| style="text-align:left;" | ${to_s(other_relationship['related_since_date'])}
| style="text-align:left;" | ${to_s(other_relationship['related_until_date'])}
| style="text-align:left;" | ${to_s(other_relationship['relationship_details'])}
% endfor
|}
% endif
% if len(other_relationships) == 0:
''No other relationships''
% endif

== Subsidies ==

* Subsidies count: ${subsidies_count}
* Total amount [EUR]: ${format_amount(subsidies_sum)}
% if len(subsidies) > 0:

{| class="wikitable sortable"
|-
! style="text-align:left;" | Identifier
! style="text-align:left;" | Year
! style="text-align:left;" | Project name
! style="text-align:right;" data-sort-type="number" | Subsidy total amount [EUR]
% for subsidy in subsidies:
|-
| style="text-align:left;" | [[${subsidy['database_identifier']}]]
| style="text-align:left;" | ${to_s(subsidy['year'])}
| style="text-align:left;" | ${to_s(subsidy['project_name'])}
| style="text-align:right;" data-sort-value="${subsidy['total_amount_in_eur']}" | ${format_amount(subsidy['total_amount_in_eur'])}
% endfor
|}
% endif

== Previous names ==

% if len(previous_names) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Previous name
! style="text-align:left;" | Since date
! style="text-align:left;" | Until date
% for previous_name in previous_names:
|-
| style="text-align:left;" | ${to_s(previous_name.previous_name)}
| style="text-align:left;" | ${to_s(previous_name.named_since_date)}
| style="text-align:left;" | ${to_s(previous_name.named_until_date)}
% endfor
|}
% endif
% if len(previous_names) == 0:
''No previous names''
% endif

== Previous addresses ==

% if len(previous_addresses) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Previous address
! style="text-align:left;" | Since date
! style="text-align:left;" | Until date
% for previous_address in previous_addresses:
|-
| style="text-align:left;" | ${to_s(previous_address.previous_address)}
| style="text-align:left;" | ${to_s(previous_address.address_since_date)}
| style="text-align:left;" | ${to_s(previous_address.address_until_date)}
% endfor
|}
% endif
% if len(previous_addresses) == 0:
''No previous addresses''
% endif

== Media mentions ==

% if len(media_mentions) > 0:
% for media_mention in media_mentions:
* ${media_mention.summary + ' ' if media_mention.summary else ''}[${media_mention.url} ${media_mention.url}]${' Last checked: ' + media_mention.last_checked_date.strftime('%Y-%m-%d') if media_mention.last_checked_date else ''}
% endfor
% endif
% if len(media_mentions) == 0:
''No media mentions''
% endif

== Other notes ==

${legal_entity.other_notes if legal_entity.other_notes else "''No other notes''"}

== Sources ==

% if len(sources) > 0:
% for source in sources:
* ${"''" + source.summary + "'' " if source.summary is not None else ''}${source.url + ' ' if source.url is not None else ''}${'(Last checked: ' + source.last_checked_date.strftime('%Y-%m-%d') + ')' if source.last_checked_date is not None else ''}
% endfor
% endif
% if len(sources) == 0:
''No sources''
% endif

[[Category:Legal entities]]
% if legal_entity.legal_entity_type is not None:
[[Category:Legal entity type ${legal_entity.legal_entity_type}]]
% endif
