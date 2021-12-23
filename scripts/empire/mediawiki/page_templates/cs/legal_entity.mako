= ${legal_entity.database_identifier} =

{| class="infobox vcard" style="width: 300px; font-size: 95%; text-align: left; border-collapse: collapse;background-color:#e9f2da;" cellpadding="6"
|-
| '''Typ právnické osoby / Legal entity type:'''
| ${legal_entity.legal_entity_type if legal_entity.legal_entity_type else ''}
|-
| '''Identifikátor (IČO, ...) / Identification number:'''
| ${legal_entity.identification_number if legal_entity.identification_number else ''}
|-
| '''Adresa / Address:'''
| ${legal_entity.address if legal_entity.address else ''}
|-
| '''Země / Country:'''
| ${legal_entity.country}
|-
| '''Datum založení / Foundation date:'''
| ${legal_entity.foundation_date if legal_entity.foundation_date else ''}
|-
| '''Datum zániku / Dissolution date:'''
| ${legal_entity.dissolution_date if legal_entity.dissolution_date else ''}
|-
|}

== Owners ==

TODO

== Other relationships ==

TODO

== Previous names ==

TODO

== Previous addresses ==

TODO

== Media mentions ==

TODO

== Notes ==

${legal_entity.other_notes if legal_entity.other_notes else "''No notes for this legal entity''"}

== References ==

TODO

[[Kategorie:Právnické osoby / Legal entities]]
% if legal_entity.legal_entity_type is not None:
[[Kategorie:Typ právnické osoby ${legal_entity.legal_entity_type} / Legal entity type ${legal_entity.legal_entity_type}]]
% endif
