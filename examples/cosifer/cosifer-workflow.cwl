class: Workflow
cwlVersion: v1.0
id: cosifer_workflow
label: cosifer-workflow
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
inputs:
  - id: data_matrix
    type: File
  - id: gmt_filepath
    type: File?
  - id: index_col
    type: int?
  - id: outdir
    type: string
  - id: separator
    type: string?
outputs:
  - id: resdir
    outputSource:
      - cosifer/resdir
    type: Directory
steps:
  - id: cosifer
    in:
      - id: data_matrix
        source: data_matrix
      - id: separator
        source: separator
      - id: index_col
        source: index_col
      - id: gmt_filepath
        source: gmt_filepath
      - id: outdir
        source: outdir
    out:
      - id: resdir
    run: ./cosifer.cwl
    label: cosifer
requirements: []
