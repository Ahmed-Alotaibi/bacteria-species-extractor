# Usage
```
Usage: extractor [OPTIONS] BACTERIOPHAGE[Name/Index] DATASET[DIRECTORY/FILE]

Extract Bacterial Species,Diseases,Disease Categories, and Abundance Changes
Related to a Bacteriophage from a Dataset

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o FILE, --output=FILE
                        Output to File FILE
  -d DELIM, --delimiter=DELIM
                        Output Using Delimiter DELIM (Can be inferred from
                        file)

Try: extractor 'Klebsiella phage st16' DIRECTORY/FILE
0 => lactobacillus phage sha1
1 => bacteriophage sp
2 => klebsiella phage kpp5665-2
3 => klebsiella phage st16
4 => klebsiella phage st846
5 => klebsiella phage st13
6 => enterobacteria phage sfi
7 => shigella phage sfii
8 => shigella phage sfiv
9 => salmonella phage st64b
10 => enterobacteria phage mep235
11 => escherichia phage henu7
12 => uc phage clone 7s_14
13 => uc phage clone 2ax_6
```
