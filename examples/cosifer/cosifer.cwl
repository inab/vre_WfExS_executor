class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: cosifer
baseCommand:
  - cosifer
inputs:
  - id: data_matrix
    type: File
    inputBinding:
      position: 0
      prefix: '-i'
  - id: separator
    type: string?
    inputBinding:
      position: 0
      prefix: '--sep='
      separate: false
  - id: index_col
    type: int?
    inputBinding:
      position: 0
      prefix: '--index'
  - id: gmt_filepath
    type: File?
    inputBinding:
      position: 0
      prefix: '--gmt_filepath'
  - id: outdir
    type: string?
    inputBinding:
      position: 0
      prefix: '-o'
outputs:
  - id: resdir
    type: Directory
    outputBinding:
      outputEval: inputs.outdir
label: cosifer
requirements:
  - class: DockerRequirement
    dockerPull: 'tsenit/cosifer:b4d5af45d2fc54b6bff2a9153a8e9054e560302e'
