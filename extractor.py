#/usr/bin/env python3

import os
import sys
from os import path
import csv
from csv import Sniffer
from optparse import OptionParser
import pdb

prog_name = 'extractor'

# Adding Cmd Options
optparser = OptionParser(prog= prog_name,
                         usage=f'Usage: {prog_name} [OPTIONS] BACTERIOPHAGE[Name/Index] DATASET[DIRECTORY/FILE]',
                         version=f'{prog_name} 2.0.0',
                         description='Extract Bacterial Species,Diseases,Disease Categories, and Abundance Changes Related to a Bacteriophage from a Dataset',
                         epilog=f'Try: {prog_name} \'Klebsiella phage st16\' DIRECTORY/FILE',
)

optparser.add_option('-o', '--output',
                 dest='output_filename',
                 default=None,
                 help='Output to File FILE',
                 metavar="FILE"
)

optparser.add_option('-d', '--delimiter',
                 dest='output_delimiter',
                 default=None,
                 help='Output Using Delimiter DELIM (Can be inferred from file)',
                 metavar="DELIM"
)

class Bacteria:
  def __init__(self):
    # Bacteriophage
    self.chosen_phage = ""
    # output File Delim
    self.delim = None
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

    '''
    # Header names of columns we're interested in
    self.headers = [
        ["disease", "disease_name", "related_disease",],
        ["microbe", "microbe_scientific_name", "organism_name"],
        ["position", "disease_type_name", "location_name",],
        ["evidence", "tendency", "relationship_name", "qualitative_outcome",],
    ]
    '''
    # Header names of columns we're interested in
    self.headers = {
        "disease": ["disease_name", "related_disease",],
        "microbe": ["microbe_scientific_name", "organism_name"],
        "position": ["disease_type_name", "location_name",],
        "evidence": ["tendency", "relationship_name", "qualitative_outcome",],
    }

    # Output header names
    self.output_header = [
        "Bacterial Species", "Genomic Pattern", "Connected Phage",
        "Human Disease", "Disease Category", "Abundance Change", "Source Database",
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
    # Names (keys) of columns that we want
    data_keys = {}
    data = []

    with open(file, 'r', encoding='utf-8-sig', newline='') as f:
      # Read a single line to find the delimiter used
      header = f.readline()
      f.seek(0)
      delim = csv.Sniffer().sniff(header, delimiters=',\t').delimiter

      # If output delim was not chosen through options, set it to the first file delim we encounter
      if self.delim is None:
        self.delim = delim

      reader = csv.DictReader(f, delimiter=delim, lineterminator='\n')
      rows = [row for row in reader]

      # Is this a column we're interested in?
      for column in list(rows[0]):
        for main_header_name, possible_header_names in self.headers.items():
          if column.lower() == main_header_name or column.lower() in possible_header_names:
            # It is!, save it's name
            data_keys[main_header_name] = column

      for row in rows:
        add = False
        microbe = row[data_keys['microbe']].lower()
        if len(microbe) <= 0:
          continue

        # Is this bacterial species under the chosen phage?
        if microbe in self.phages[self.chosen_phage]:
          add = True

        #or atleast related to the same family that other species are?
        elif microbe in list(self.bacteria_families):
          if len(set(self.bacteria_families[microbe]) & set(self.phages[self.chosen_phage])) > 0:
            add = True

        # If it's a yes, then add it in the same order as output_header
        if add:
          pattern = None
          for pat, bacteriophage in self.patterns.items():
            if self.chosen_phage in bacteriophage:
              pattern = pat
              break

          # Bacterial Species    Genomic Pattern    Connected Phage    Human Disease    Disease Category    Abundance Change    Source Database
          data.append([row[data_keys["microbe"]].lower(),     # Bacterial Species 
                       pattern,                               # Genomic Pattern
                       self.chosen_phage,                     # Connected Phage
                       row[data_keys["disease"]].lower(),     # Human Disease
                       row[data_keys["position"]].lower(),    # Diseases Category
                       row[data_keys["evidence"]].lower(),    # Abundance Change
                       path.splitext(path.basename(file))[0]] # Source Database
          )

    return data

  # Walk the dataset directory and search each file
  def search_bacteria_in_dir(self, directory):
    file_and_data = {}
    for root, unused, files in os.walk(directory):
      for f in files:
        data = self.search_bacteria_in_file(path.join(root, f))
        if len(data) > 0:
          file_and_data[path.splitext(f)[0]] = data

    return file_and_data

  # Output [ct]sv
  def write_csv(self, source, data, output, print_headers=True):
    # DIR/FILE.EXT => FILE
    source = path.splitext(path.basename(source))[0]

    writer = csv.writer(output, delimiter=self.delim, lineterminator='\n')
    if print_headers:
      writer.writerow(self.output_header)

    writer.writerows(data)

def usage(optparser):
  optparser.print_help()
  for i, v in enumerate(Bacteria().phages):
    print(f"{i} => {v}", file=sys.stderr)
  sys.exit(1)


def main():
  opts, args = optparser.parse_args()
  if len(args) != 2:
    usage(optparser)

  output = sys.stdout if opts.output_filename is None else open(opts.output_filename, 'w', encoding='utf-8')

  phage_species, dataset = args[:2]


  bact = Bacteria()
  if opts.output_delimiter is not None:
    bact.delim = opts.output_delimiter.replace(r'\t', '\t')

  if not bact.select_phage(phage_species):
    print(f"Invalid phage name/index => {phage_species}\n", file=sys.stderr)
    usage(progname)

  #pdb.set_trace()

  if path.isdir(dataset):
    dir_data = bact.search_bacteria_in_dir(dataset)

    for col in bact.output_header:
      print(col, end=bact.delim, file=output)
    print(file=output)

    for filename, data in dir_data.items():
      bact.write_csv(filename, data, output, print_headers=False)

  else:
    file_data = bact.search_bacteria_in_file(dataset)
    bact.write_csv(dataset, file_data, output)

  if opts.output_filename is not None:
    output.close()

if __name__ == '__main__':
  try:
    main()
  except:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(1)
