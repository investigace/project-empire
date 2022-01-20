= Přehled právnických osob / Legal entities overview =

% for group in legal_entities_by_country:
== ${group['country_name']} ==

{| class="wikitable sortable"
|-
!
! Typ právnické osoby / Legal entity type
! Země / Country
! Identifikátor (IČO, ...) / Identification number
! style="text-align:right;" data-sort-type="number" | Nalezených dotací / Subsidies found
! style="text-align:right;" data-sort-type="number" | Suma dotací [EUR] / Subsidies sum [EUR]
% for legal_entity in group['legal_entities']:
|-
| [[${legal_entity.database_identifier}]]
| ${to_s(legal_entity.legal_entity_type)}
| ${to_s(legal_entity.country)}
| ${to_s(legal_entity.identification_number)}
| style="text-align:right;" | ${stats_by_legal_entity[legal_entity.database_identifier]['subsidies_count']}
| style="text-align:right;" data-sort-value="${stats_by_legal_entity[legal_entity.database_identifier]['subsidies_sum']}" | ${format_amount(stats_by_legal_entity[legal_entity.database_identifier]['subsidies_sum'])}
% endfor
|}
% endfor
