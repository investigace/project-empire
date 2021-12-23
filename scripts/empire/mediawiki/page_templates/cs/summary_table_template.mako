= Template:Empire summary table =

{| class="wikitable"
|-
! style="text-align:left;" | Země / Country
! style="text-align:right;" | Nalezených právnických osob / Found legal entities
! style="text-align:right;" | Nalezených fyzických osob / Found people
! style="text-align:right;" | Nalezených dotací / Found subsidies
! style="text-align:right;" | Suma dotací / Subsidies sum
% for country in countries:
|-
| style="text-align:left;" | ${country['name']}
| style="text-align:right;" | ${("[[Přehled právnických osob / Legal entities overview#" + country['name'] + " | " + str(country['legal_entities_count'])) if country['legal_entities_count'] > 0 else '0'}
| style="text-align:right;" | ${("[[Přehled fyzických osob / People overview#" + country['name'] + " | " + str(country['people_count'])) if country['people_count'] > 0 else '0'}
| style="text-align:right;" | TODO
| style="text-align:right;" | TODO
% endfor
|-
! style="text-align:left;" | Celkem / Total
! style="text-align:right;" | ${totals['legal_entities_count']}
! style="text-align:right;" | ${totals['people_count']}
! style="text-align:right;" | TODO
! style="text-align:right;" | TODO
|}
