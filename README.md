# Usage
```
extractor.py BACTRIOPHAGE[NAME/INDEX] DATASET[DIRECTORY/FILE]
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
