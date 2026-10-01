#/usr/bin/env python3

import os
import sys
from os import path

#   0 => Bacteriophage
# > 0 => Bacteria

class Bacteria:
  def __init__(self):
    self.chosen_phage = -1
    self.patterns = [
        [ "HNH"         , "Phage_portal", "Phage_capsid", ],
        [ "Terminase_1" , "Phage_portal", "Phage_capsid", ],
        [ "Phage_capsid", "Phage_portal", "Terminase_1",  ],
    ]
    self.phages = [
        "Lactobacillus phage Sha1",
        "Bacteriophage sp",
        "Klebsiella phage KPP5665-2",
        "Klebsiella phage ST16",
        "Klebsiella phage ST846",
        "Klebsiella phage ST13",
        "Enterobacteria phage SfI",
        "Shigella phage SfII",
        "Shigella phage SfIV",
        "Salmonella phage ST64B",
        "Enterobacteria phage mEp235",
        "Escherichia phage Henu7",
        "UC phage clone 7S_14",
        "UC phage clone 2AX_6",
    ]
    self.bacteria = [
        ["Pediococcus pentosaceus",],
        ["Latilactobacillus curvatus", "Latilactobacillus sakei",],
        ["Pantoea vagans", "Citrobacter freundii",],
        ["Pantoea vagans", "Citrobacter freundii",],
        ["Citrobacter braakii", "Citrobacter tructae",],
        ["Citrobacter amalonaticus", "Enterobacter hormaechei", "Salmonella enterica",],
        ["Escherichia albertii",],
        ["Escherichia albertii",],
        ["Escherichia albertii",],
        ["Escherichia albertii",],
        ["Cronobacter sakazakii",],
        ["Enterobacter soli", "Pluralibacter gergoviae", "Klebsiella michiganensis",],
        ["Enterobacter soli", "Pluralibacter gergoviae", "Klebsiella michiganensis",],
        ["Enterobacter soli", "Pluralibacter gergoviae", "Klebsiella michiganensis",],
    ]

    # Case in-sensitve
    self.headers = [
        ["disease", "disease_name", "related_disease",],
        ["microbe", "microbe_scientific_name", "organism_name"],
        ["position", "disease_subtype", "location_name",],
        ["evidence", "tendency", "relationship_name", "qualitative_outcome",],
    ]

  # ph = string/index
  def select_phage(self, ph):
    if ph.isdigit():
      self.chosen_phage = int(ph)
      if self.chosen_phage < 0 or self.chosen_phage >= len(self.phages):
        return False

      return True
    else:
      for i, p in enumerate(self.phages):
        if ph == p:
          self.chosen_phage = i
          return True

      return False

  def search_bacteria_in_file(self, file):
    columns = {}
    data = {h[0]: [] for h in self.headers}

    with open(file, encoding='utf-8') as f:
      content = [line.lower() for line in f]
      #print(f"{content[0]}")
      for i, h in enumerate(content[0].split('\t')):
        #print(f"{file} => {h}")
        for exp_headers in self.headers:
          if h.strip() in exp_headers:
            #print(f"{file} => columns[{exp_headers[0]}] = {i}")
            columns[exp_headers[0]] = i

      if len(list(columns)) != 4:
        print(f"{file} => {list(columns)}")

      # Skip header
      content = content[1:]

      for line in content:
        values = str(line).split('\t')
        #print(f"microbe: {values[columns[self.headers[1][0]]].strip()}")
        if values[columns[self.headers[1][0]]].strip() not in self.bacteria[self.chosen_phage]:
          continue
        for k, v in columns.items():
          #print(f"{file} => data[{k}] = {values[v].strip()}")
          data[k].append(values[v].strip())

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
  print(f"Usage: {progname} BACTERIOPHAGE[name/index] DATASET_DIRECTORY", file=sys.stderr)
  for i, v in enumerate(Bacteria().phages):
    print(f"{i} => {v}")
  sys.exit(1)

def main():
  if(len(sys.argv) < 3):
    usage(sys.argv[0])

  progname, phage_species, dataset_directory = sys.argv[:3]

  bact = Bacteria()

  if not bact.select_phage(phage_species):
    print(f"Invalid phage name/index => {phage_species}\n", file=sys.stderr)
    usage(progname)

  fdata = bact.search_bacteria_in_dir(dataset_directory)

  for filename, data in fdata.items():
    print(f"{filename}:")
    for column, content in data.items():
      print(f"{column} => {content}")

if __name__ == '__main__':
  try:
    main()
  except BrokenPipeError:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(1)
