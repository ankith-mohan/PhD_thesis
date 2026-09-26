# PhD Thesis

## Techniques for computing and approximating large optimization problems in quantum information

**Author:** Ankith Mohan  
**Institution:** Virginia Tech  
**Degree:** Ph.D. in Computer Science and Application  
**Date:** July 9, 2026  
**Advisor:** Jamie Sikora

This repository contains the LaTeX source, figures, bibliography, and supporting files for my Ph.D. dissertation.

## Official dissertation

The officially published version of the dissertation is available through Virginia Tech's VTechWorks repository:

[View the official dissertation](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/88cdb9a9-f9f8-4993-82f1-6715df8d03ee/content)

The university-hosted version should be treated as the archival version of record.

## Repository contents

- `Ankith_Mohan_PhD_thesis.tex` — main LaTeX source
- `contents/` — chapter and section source files
- `figs/` — figures used in the dissertation
- `ref.bib` — bibliography
- `VTthesis.cls` — Virginia Tech thesis class
- supporting scripts and auxiliary source files

## Dissertation topics

The dissertation studies computational techniques for large optimization problems in quantum information, including:

- optimization over separable quantum states
- semidefinite programming and dimension reduction
- quantum state discrimination
- quantum changepoint problems
- quantum error classification
- state exclusion
- memory-constrained quantum protocols

## Building the thesis

The thesis can be compiled from the main source file:

```bash
latexmk -lualatex Ankith_Mohan_PhD_thesis.tex
