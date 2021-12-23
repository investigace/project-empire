= Template:Empire summary table =

{| class="wikitable"
|-
! style="text-align:left;" | Country
! style="text-align:right;" | Found legal entities
! style="text-align:right;" | Found people
! style="text-align:right;" | Found subsidies
! style="text-align:right;" | Subsidies sum
% for country in countries:
|-
| style="text-align:left;" | ${country['name']}
| style="text-align:right;" | ${("[[Legal entities overview#" + country['name'] + " | " + str(country['legal_entities_count']) + "]]") if country['legal_entities_count'] > 0 else '0'}
| style="text-align:right;" | ${("[[People overview#" + country['name'] + " | " + str(country['people_count']) + "]]") if country['people_count'] > 0 else '0'}
| style="text-align:right;" | TODO
| style="text-align:right;" | TODO
% endfor
|-
! style="text-align:left;" | Total
! style="text-align:right;" | ${totals['legal_entities_count']}
! style="text-align:right;" | ${totals['people_count']}
! style="text-align:right;" | TODO
! style="text-align:right;" | TODO
|}
