= Template:Empire summary table =

{| class="wikitable"
|-
! style="text-align:left;" | Země / Country
! style="text-align:right;" | Nalezených právnických osob / Found legal entities
! style="text-align:right;" | Nalezených fyzických osob / Found people
! style="text-align:right;" | Nalezených dotací / Found subsidies
! style="text-align:right;" | Suma dotací / Subsidies sum
!
% for country in countries:
|-
| style="text-align:left;" | ${country['name']}
| style="text-align:right;" | ${country['legal_entities_count']}
| style="text-align:right;" | ${country['people_count']}
| style="text-align:right;" | TODO
| style="text-align:right;" | TODO
| style="text-align:left;" | [[Přehled právnických osob / Legal entities overview#${country['name']} | Zobrazit právnické osoby]] / [[Přehled fyzických osob / People overview#${country['name']} | Zobrazit fyzické osoby]] / [[Přehled dotací / Subsidies overview#${country['name']} | Zobrazit dotace]]
% endfor
|-
! style="text-align:left;" | Celkem / Total
! style="text-align:right;" | ${totals['legal_entities_count']}
! style="text-align:right;" | ${totals['people_count']}
! style="text-align:right;" | TODO
! style="text-align:right;" | TODO
!
|}
