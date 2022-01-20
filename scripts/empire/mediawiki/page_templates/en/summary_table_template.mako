= Template:Empire summary table =

{| class="wikitable"
|-
! style="text-align:left;" | Country
! style="text-align:right;" | Found legal entities
! style="text-align:right;" | Found people
! style="text-align:right;" | Found subsidies
! style="text-align:right;" | Subsidies sum [EUR]
% for country in countries:
|-
| style="text-align:left;" | ${country['name']}
| style="text-align:right;" | ${("[[Legal entities overview#" + country['name'] + " | " + str(country['legal_entities_count']) + "]]") if country['legal_entities_count'] > 0 else '0'}
| style="text-align:right;" | ${("[[People overview#" + country['name'] + " | " + str(country['people_count']) + "]]") if country['people_count'] > 0 else '0'}
| style="text-align:right;" | ${("[[Subsidies overview#" + country['name'] + " | " + str(country['subsidies_count']) + "]]") if country['subsidies_count'] > 0 else '0'}
| style="text-align:right;" | ${format_amount(country['subsidies_sum'])}
% endfor
|-
! style="text-align:left;" | Total
! style="text-align:right;" | ${totals['legal_entities_count']}
! style="text-align:right;" | ${totals['people_count']}
! style="text-align:right;" | ${totals['subsidies_count']}
! style="text-align:right;" | ${format_amount(totals['subsidies_sum'])}
|}
