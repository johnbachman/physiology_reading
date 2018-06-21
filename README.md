# Machine reading for physiological mechanisms

## MESH data

MESH data downloaded on 6/20/2018 from
NCBI [here.](ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/asciimesh/)

Files:
* d2018.bin. Descriptors a.k.a. subject headings. A given descriptor may
  appear at several locations in the hierarchical tree. Descriptors contain
  both alphanumerical IDs and one or more tree locations.
* q2018.bin. Qualifiers, can be applied to descriptors to narrow down the
  topic. Not all descriptor/qualifier combinations are allowed.
* c2018.bin. Supplements. Not part of the controlled vocabulary as such, but
  provide links to the closest fitting descriptor. Many refer to small
  molecules.

## Data extracted from MESH descriptors

`mesh_to_yml.py` parses the ASCII descriptor file `d2018.bin` and propagates
the following information in to the yml ontology file:

* Name (DescriptorName, MH)
* Unique identifier (DescriptorUI, UI)
* Tree numbers/locations (MN)
* Examples/terms (TermList, ENTRY, PRINT ENTRY)
* Description (ScopeNote, MS)

Other information that is not currently extracted includes:

* Allowable qualifiers (AQ)
* Pharmacological actions
* ConceptList, ConceptRelationList

In the assembled YAML ontology, each level is a list of dicts; each dict
contains a key which is either the MESH location of the subtree or
`OntologyNode`, containing the info for the containing tree number.

Example:

```
- MESH:
  - D03:
    - D03.633:
      - D03.633.100:
        - D03.633.100.221:
          - OntologyNode:
              descriptions: []
              examples:
              - Benzoxazoles
              name: Benzoxazoles
          - D03.633.100.221.173:
            - OntologyNode:
                descriptions:
                - An ionophorous, polyether antibiotic from Streptomyces
                  chartreusensis.  It binds and transports CALCIUM and other
                  divalent cations across membranes and uncouples oxidative
                  phosphorylation while inhibiting ATPase of rat liver
                  mitochondria. The substance is used mostly as a biochemical
                  tool to study the role of divalent cations in various
                  biological systems.
                examples:
                - Calcimycin
                - A-23187
                - A23187
                - Antibiotic A23187
                - A 23187
                - A23187, Antibiotic
                name: Calcimycin
```

