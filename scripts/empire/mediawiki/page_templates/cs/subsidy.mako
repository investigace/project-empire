= ${subsidy.database_identifier} =

{| class="wikitable"
|-
! style="text-align:left;" | Identifikátor / Identifier
| ${subsidy.database_identifier}
|-
! style="text-align:left;" | Příjemce / Beneficiary
| [[${subsidy.receiving_legal_entity.database_identifier}]]
|-
! style="text-align:left;" | Kód projektu / Project code
| ${to_s(subsidy.project_code)}
|-
! style="text-align:left;" | Název projektu / Project name
| ${to_s(subsidy.project_name)}
|-
! style="text-align:left;" | Kód programu / Programme code
| ${to_s(subsidy.programme_code)}
|-
! style="text-align:left;" | Název programu / Programme name
| ${to_s(subsidy.programme_name)}
|-
! style="text-align:left;" | Rok / Year
| ${to_s(subsidy.year)}
|-
! style="text-align:left;" | Celková částka dotace v EUR / Subsidy total amount in EUR
| ${format_amount(payments_sum)}
|}

== Úhrady / Payments ==

% if len(payments) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Poskytovatel / Provider
! style="text-align:left;" | Rok / Year
! style="text-align:left;" | Původní měna / Original currency
! style="text-align:left;" | Poznámky / Notes
! style="text-align:right;" | Částka v původní měně / Amount in original currency
! style="text-align:right;" | Částka v EUR / Amount in EUR
% for payment in payments:
|-
| style="text-align:left;" | ${to_s(payment.provider)}
| style="text-align:left;" | ${to_s(payment.year)}
| style="text-align:left;" | ${to_s(payment.original_currency)}
| style="text-align:left;" | ${to_s(payment.notes)}
| style="text-align:right;" | ${format_amount(payment.amount_in_original_currency)}
| style="text-align:right;" | ${format_amount(payment.amount_in_eur)}
% endfor
|}
% endif
% if len(payments) == 0:
''Nemá žádné úhrady / Does not have any payments''
% endif

== Poznámky / Notes ==

${subsidy.notes if subsidy.notes else "''Žádné poznámky / No notes''"}

== Zdroje / Sources ==

% if len(sources) > 0:
% for source in sources:
* ${"''" + source.summary + "'' " if source.summary is not None else ''}${source.url + ' ' if source.url is not None else ''}${'(Naposledy kontrolováno / Last checked: ' + source.last_checked_date.strftime('%Y-%m-%d') + ')' if source.last_checked_date is not None else ''}
% endfor
% endif
% if len(sources) == 0:
''Bez zdrojů / No sources''
% endif

[[Kategorie:Dotace / Subsidies]]
