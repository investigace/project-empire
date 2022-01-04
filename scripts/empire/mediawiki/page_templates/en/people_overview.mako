= People overview =

% for group in people_by_country:
== ${group['country_name']} ==

{| class="wikitable sortable"
|-
!
! Nationality
! Residence country
! Residence city
% for person in group['people']:
|-
| [[${person.database_identifier}]]
| ${person.nationality if person.nationality else ''}
| ${person.residence_country if person.residence_country else ''}
| ${person.residence_city if person.residence_city else ''}
% endfor
|}
% endfor
