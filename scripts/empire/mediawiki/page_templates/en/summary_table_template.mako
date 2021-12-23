= Template:Empire summary table =

{| class="wikitable"
|-
! style="text-align:left;" | Country
! style="text-align:right;" | Found legal entities
! style="text-align:right;" | Found people
! style="text-align:right;" | Found subsidies
! style="text-align:right;" | Subsidies sum
!
% for country in countries:
|-
| style="text-align:left;" | ${country['name']}
| style="text-align:right;" | ${country['legal_entities_count']}
| style="text-align:right;" | ${country['people_count']}
| style="text-align:right;" | TODO
| style="text-align:right;" | TODO
| style="text-align:left;" | [[Legal entities overview#${country['name']} | Show legal entities]] / [[People overview#${country['name']} | Show people]] / [[Subsidies overview#${country['name']} | Show subsidies]]
% endfor
|-
! style="text-align:left;" | Total
! style="text-align:right;" | ${totals['legal_entities_count']}
! style="text-align:right;" | ${totals['people_count']}
! style="text-align:right;" | TODO
! style="text-align:right;" | TODO
!
|}
