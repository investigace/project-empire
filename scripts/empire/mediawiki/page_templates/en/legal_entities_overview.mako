= Legal entities overview =

% for group in legal_entities_by_country:
== ${group['country_name']} ==

{| class="wikitable sortable"
|-
!
! Legal entity type
! Country
! Identification number
! Subsidies found
! Subsidies sum
% for legal_entity in group['legal_entities']:
|-
| [[${legal_entity.database_identifier}]]
| ${legal_entity.legal_entity_type if legal_entity.legal_entity_type else ''}
| ${legal_entity.country}
| ${legal_entity.identification_number if legal_entity.identification_number else ''}
| TODO
| TODO
% endfor
|}
% endfor
