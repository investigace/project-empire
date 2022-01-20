= Legal entities overview =

% for group in legal_entities_by_country:
== ${group['country_name']} ==

{| class="wikitable sortable"
|-
!
! Legal entity type
! Country
! Identification number
! style="text-align:right;" data-sort-type="number" | Subsidies found
! style="text-align:right;" data-sort-type="number" | Subsidies sum [EUR]
% for legal_entity in group['legal_entities']:
|-
| [[${legal_entity.database_identifier}]]
| ${legal_entity.legal_entity_type if legal_entity.legal_entity_type else ''}
| ${legal_entity.country}
| ${legal_entity.identification_number if legal_entity.identification_number else ''}
| style="text-align:right;" | ${stats_by_legal_entity[legal_entity.database_identifier]['subsidies_count']}
| style="text-align:right;" data-sort-value="${stats_by_legal_entity[legal_entity.database_identifier]['subsidies_sum']}" | ${format_amount(stats_by_legal_entity[legal_entity.database_identifier]['subsidies_sum'])}
% endfor
|}
% endfor
