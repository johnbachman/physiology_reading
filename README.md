# Machine reading for physiological mechanisms

## MESH data

MESH data downloaded on 6/20/2018 from
NCBI [here.](ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/xmlmesh/)

Files:
* desc2018.xml. Descriptors a.k.a. subject headings. A given descriptor may
  appear at several locations in the hierarchical tree. Descriptors contain
  both alphanumerical IDs and one or more tree locations.
* qual2018.xml. Qualifiers, can be applied to descriptors to narrow down the
  topic. Not all descriptor/qualifier combinations are allowed.
* supp2018.xml. Supplements. Not part of the controlled vocabulary as such, but
  provide links to the closest fitting descriptor. Many refer to small
  molecules.

## Data extracted from MESH

For each descriptor record, extracts
* DescriptorName
* Allowable qualifiers (AQ)
* TermList/Entries (ENTRY, PRINT ENTRY)
* Tree numbers (MN)
* DescriptorUI (UI)

* (ScopeNote?)
* (Pharmacological actions (other descriptors))
* ConceptList
* (ConceptRelationList)
* Description

Root node: MESH

Each level is a list of dicts; each dict containing a list of dicts.

- UN
  - weather:
    - Ontology: (for weather)
    - precipitation:
      - OntologyNode:
        name: precipitation
        examples:
          - foo
          - bar
        descriptions:
          - asdfasdfasdfa
      - rain:
        - OntologyNode:
          name: rain
          examples:
            - rainfall

