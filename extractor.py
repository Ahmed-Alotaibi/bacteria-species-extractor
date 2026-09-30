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
    lines = []
    with open(file, "r", encoding='utf-8') as content:
      for line in content:
        for b in self.bacteria[self.chosen_phage]:
          if b in line:
            lines += (str(line.strip()).split('\t'))

    return lines

  def search_bacteria_in_dir(self, directory):
    file_and_lines = {}
    for root, dirs, files in os.walk(directory):
      for f in files:
        lines = self.search_bacteria_in_file(path.join(root, f))
        if len(lines) > 0:
          file_and_lines.update({ f : lines })

    return file_and_lines

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
  file_list = []

  if not bact.select_phage(phage_species):
    print(f"Invalid phage name/index => {phage_species}\n", file=sys.stderr)
    usage(progname)

  kv = bact.search_bacteria_in_dir(dataset_directory)

  for k, v in kv.items():
    print(f"{k}:\n{v}\n")

if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)
