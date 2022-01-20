= Subsidies overview =

% for group in subsidies_by_country:
== ${group['country_name']} ==

{| class="wikitable sortable"
|-
! Identifier
! Beneficiary
! Year
! style="text-align:right;" data-sort-type="number" | Subsidy total amount in EUR
% for subsidy in group['subsidies']:
|-
| [[${subsidy.database_identifier}]]
| [[${subsidy.receiving_legal_entity.database_identifier}]]
| ${to_s(subsidy.year)}
| style="text-align:right;" data-sort-value="${stats_by_subsidy[subsidy.database_identifier]['total_amount_in_eur']}" | ${format_amount(stats_by_subsidy[subsidy.database_identifier]['total_amount_in_eur'])}
% endfor
|}
% endfor
