= Legal entities overview =

% for group in legal_entities_by_country:
== ${group['country_name']} ==

{| class="wikitable sortable"
|-
!  !! Legal entity type !! Country !! Identification number !! Owners !! Subsidies found !! Subsidies sum
% for legal_entity in group['legal_entities']:
|-
| [[${legal_entity.database_identifier}]] || ${legal_entity.legal_entity_type} || ${legal_entity.country} || ${legal_entity.identification_number} || TODO || TODO || TODO
% endfor
|}
% endfor
