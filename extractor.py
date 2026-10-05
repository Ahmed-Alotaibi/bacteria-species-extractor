#/usr/bin/env python3

import os
import sys
from os import path

#   0 => Bacteriophage
# > 0 => Bacteria

class Bacteria:
  def __init__(self):
    self.chosen_phage = ""
    self.patterns = {
        "hnh"                                       : ["lactobacillus phage sha1",],
        "terminase_1, phage_portal, phage_capsid"   : [
            "bacteriophage sp",
            "klebsiella phage kpp5665-2",
            "klebsiella phage st16",
            "klebsiella phage st13",
            "enterobacteria phage sfi",
            "shigella phage sfii",
            "shigella phage sfiv",
            "salmonella phage st64b",
            "enterobacteria phage mep235",
            "escherichia phage henu7",
            "uc phage clone 7s_14",
            "uc phage clone 2ax_6",
        ],
        "phage_capsid, phage_portal, terminase_1"   : ["klebsiella phage st846", "klebsiella phage st13",],
    }
    self.phages = {
        "lactobacillus phage sha1"      : ["pediococcus pentosaceus",],
        "bacteriophage sp"              : ["latilactobacillus curvatus", "latilactobacillus sakei",],
        "klebsiella phage kpp5665-2"    : ["pantoea vagans", "citrobacter freundii",],
        "klebsiella phage st16"         : ["pantoea vagans", "citrobacter freundii",],
        "klebsiella phage st846"        : ["citrobacter braakii", "citrobacter tructae",],
        "klebsiella phage st13"         : ["citrobacter amalonaticus", "enterobacter hormaechei", "salmonella enterica",],
        "enterobacteria phage sfi"      : ["escherichia albertii",],
        "shigella phage sfii"           : ["escherichia albertii",],
        "shigella phage sfiv"           : ["escherichia albertii",],
        "salmonella phage st64b"        : ["escherichia albertii",],
        "enterobacteria phage mep235"   : ["cronobacter sakazakii",],
        "escherichia phage henu7"       : ["enterobacter soli", "pluralibacter gergoviae", "klebsiella michiganensis",],
        "uc phage clone 7s_14"          : ["enterobacter soli", "pluralibacter gergoviae", "klebsiella michiganensis",],
        "uc phage clone 2ax_6"          : ["enterobacter soli", "pluralibacter gergoviae", "klebsiella michiganensis",],
    }
    self.bacteria_families = {
        "latilactobacillus"   : ["latilactobacillus curvatus", "latilactobacillus sakei",],
        "pediococcus"         : ["pediococcus pentosaceus",],
        "pantoea"             : ["pantoea vagans",],
        "citrobacter freundii": ["citrobacter freundii", "citrobacter braakii",],
        "citrobacter"         : ["citrobacter tructae", "citrobacter amalonaticus",],
        "enterobacter"        : ["enterobacter hormaechei", "enterobacter soli",],
        "salmonella"          : ["salmonella enterica",],
        "escherichia"         : ["escherichia albertii",],
        "pluralibacter"       : ["pluralibacter gergoviae",],
        "cronobacter"         : ["cronobacter sakazakii",],
        "klebsiella"          : ["klebsiella michiganensis",],
    }

    # Case in-sensitve
    self.headers = [
        ["disease", "disease_name", "related_disease",],
        ["microbe", "microbe_scientific_name", "organism_name"],
        ["position", "disease_type_name", "location_name",],
        ["evidence", "tendency", "relationship_name", "qualitative_outcome",],
    ]

    self.output_header = [
        "Bacterial Species",
        "Genomic Pattern",
        "Connected Phage",
        "Human Disease",
        "Disease Category",
        "Abundance Change",
        "Source Database",
    ]

  # ph = string/index
  def select_phage(self, ph):
    if ph.isdigit():
      idx = int(ph)
      if idx < 0 or idx >= len(self.phages):
        return False

      self.chosen_phage = list(self.phages)[idx]
      return True
    else:
      if ph.lower() in list(self.phages):
        self.chosen_phage = ph.lower()
        return True

      return False

  def search_bacteria_in_file(self, file):
    columns = {h[0]: -1 for h in self.headers}
    data    = []

    with open(file, encoding='utf-8') as f:
      content = [line.lower() for line in f]
      for i, h in enumerate(content[0].split('\t')):
        for header in self.headers:
          if h.strip() in header:
              columns[header[0]] = i

      # Skip header
      content = content[1:]

      for line in content:
        values = str(line).split('\t')
        microbe = values[columns["microbe"]].strip()
        if len(microbe) <= 0:
          continue

        #print(f"{microbe} ==? {self.phages[self.chosen_phage]}")
        #print(f"{microbe} ==? {list(self.bacteria_families)}")

        # If it's in the bacteriophage, add it
        if microbe in self.phages[self.chosen_phage]:
          data.append([values[x].strip() for x in columns.values()])
          continue

        # If not, check that it belongs to the same family of those in the bacteriophage
        if microbe in list(self.bacteria_families):
          #print(f"{set(self.bacteria_families[microbe])}", file=sys.stderr)
          #print(f"{set(self.phages[self.chosen_phage])}", file=sys.stderr)
          if len(set(self.bacteria_families[microbe]) & set(self.phages[self.chosen_phage])) > 0:
            data.append([values[x].strip() for x in columns.values()])

    return data

  def search_bacteria_in_dir(self, directory):
    file_and_data = {}
    for root, dirs, files in os.walk(directory):
      for f in files:
        data = self.search_bacteria_in_file(path.join(root, f))
        if len(data) > 0:
          file_and_data[f] = data

    return file_and_data

def usage(progname):
  print(f"Usage: {progname} BACTERIOPHAGE[name/index] DATASET[DIRECTORY/FILE]", file=sys.stderr)
  for i, v in enumerate(Bacteria().phages):
    print(f"{i} => {v}")
  sys.exit(1)

def main():
  if(len(sys.argv) < 3):
    usage(sys.argv[0])

  progname, phage_species, dataset = sys.argv[:3]

  bact = Bacteria()

  if not bact.select_phage(phage_species):
    print(f"Invalid phage name/index => {phage_species}\n", file=sys.stderr)
    usage(progname)

  if path.isdir(dataset):
    dir_data = bact.search_bacteria_in_dir(dataset)
    for col in bact.output_header:
      print(col, end='\t')
    print()
    for filename, data in dir_data.items():
      for data_row_list in data:
        print(data_row_list[1], end='\t')
        for k, v in bact.patterns.items():
          if bact.chosen_phage in v:
            print(k, end='\t')
            break
        print(bact.chosen_phage, end='\t')
        print(data_row_list[0], end='\t')
        print(data_row_list[2], end='\t')
        print(data_row_list[3], end='\t')
        print(filename)
  else:
    file_data = bact.search_bacteria_in_file(dataset)
    for col in bact.output_header:
      print(col, end='\t')
    print()

    for data_row_list in file_data:
      print(data_row_list[1], end='\t')
      for k, v in bact.patterns.items():
        if bact.chosen_phage in v:
          print(k, end='\t')
          break
      print(bact.chosen_phage, end='\t')
      print(data_row_list[0], end='\t')
      print(data_row_list[2], end='\t')
      print(data_row_list[3], end='\t')
      print(dataset)

if __name__ == '__main__':
  try:
    main()
  except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(1)
