# Usage
```
extractor.py BACTERIOPHAGE[name/index] DATASET[DIRECTORY/FILE]
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
13 => uc phage clone 2ax_6sage: extractor.py BACTERIOPHAGE[name/index] DATASET[DIRECTORY/FILE]
```
## Note: 0-based index - Tab seperated output

## Example Usage and output
```
python3 extractor.py "Klebsiella phage st13" data/HMDAD.txt > Klebsiella-phage-st13.tsv
```
```
Bacterial Species	Genomic Pattern	Connected Phage	Human Disease	Disease Category	Abundance Change	Source Database	
enterobacter hormaechei	terminase_1, phage_portal, phage_capsid	klebsiella phage st13	necrotizing enterocolitis	gastrointestinal tract	decrease	data/HMDAD.txt

citrobacter	terminase_1, phage_portal, phage_capsid	klebsiella phage st13	necrotizing enterocolitis	gastrointestinal tract	increase	data/HMDAD.txt

klebsiella	terminase_1, phage_portal, phage_capsid	klebsiella phage st13	necrotizing enterocolitis	gastrointestinal tract	decrease	data/HMDAD.txt

klebsiella	terminase_1, phage_portal, phage_capsid	klebsiella phage st13	systemic inflammatory response syndrome	gastrointestinal tract	decrease	data/HMDAD.txt
```
