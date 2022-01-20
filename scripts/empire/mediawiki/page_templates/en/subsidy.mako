= ${subsidy.database_identifier} =

{| class="wikitable"
|-
! style="text-align:left;" | Identifier
| ${to_s(subsidy.database_identifier)}
|-
! style="text-align:left;" | Beneficiary
| [[${subsidy.receiving_legal_entity.database_identifier}]]
|-
! style="text-align:left;" | Project code
| ${to_s(subsidy.project_code)}
|-
! style="text-align:left;" | Project name
| ${to_s(subsidy.project_name)}
|-
! style="text-align:left;" | Programme code
| ${to_s(subsidy.programme_code)}
|-
! style="text-align:left;" | Programme name
| ${to_s(subsidy.programme_name)}
|-
! style="text-align:left;" | Year
| ${to_s(subsidy.year)}
|-
! style="text-align:left;" | Subsidy total amount in EUR
| ${format_amount(payments_sum)}
|}

== Payments ==

% if len(payments) > 0:
{| class="wikitable sortable"
|-
! style="text-align:left;" | Provider
! style="text-align:left;" | Year
! style="text-align:left;" | Original currency
! style="text-align:left;" | Notes
! style="text-align:right;" | Amount in original currency
! style="text-align:right;" | Amount in EUR
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
''Does not have any payments''
% endif

== Notes ==

${subsidy.notes if subsidy.notes else "''No notes''"}

== Sources ==

% if len(sources) > 0:
% for source in sources:
* ${"''" + source.summary + "'' " if source.summary is not None else ''}${source.url + ' ' if source.url is not None else ''}${'(Last checked: ' + source.last_checked_date.strftime('%Y-%m-%d') + ')' if source.last_checked_date is not None else ''}
% endfor
% endif
% if len(sources) == 0:
''No sources''
% endif

[[Kategorie:Subsidies]]
