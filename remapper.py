import os, sys, datetime, re, ntpath

def main():
	if len(sys.argv) < 2:
		print("Invalid arguments: Usage:", sys.argv[0], "<command>\nValid Commands: merge, apply")
		sys.exit(1)

	command = sys.argv[1]

	if command == "merge":
		merge()
	elif command == "apply":
		apply()
	else:
		print("Command", command, "does not exist")

def merge():
	if len(sys.argv) < 4:
		print("Invalid arguments: Usage:", sys.argv[0], "merge <mergefrom> <mergewith>")
		sys.exit(1)

	mergefrom = sys.argv[2]
	mergeto = sys.argv[3]

	from_dict = into_dict(mergefrom)
	to_dict = into_dict(mergeto)

	merge_dicts(from_dict, to_dict)

def apply():
	if len(sys.argv) < 4:
		print("Invalid arguments: Usage:", sys.argv[0], "apply <target> <mappings>")
		sys.exit(1)

	target = sys.argv[2]
	mappings = sys.argv[3]
	mapping_dict = into_dict(mappings)
	output_dir = target + "/" +"output/remap-{date:%Y%m%d%H%M%S}".format(date = datetime.datetime.now())

	apply_mappings(target, mapping_dict, output_dir)

def into_dict(file):
	out_dict = {}

	with open(file, mode="r", encoding="utf-8") as f:
		for line in f:
			toks = line.strip().split(",")
			if len(toks) != 2: 
				continue

			out_dict[toks[0]] = toks[1]

	return out_dict

def merge_dicts(from_dict, to_dict):
	ignore = []
	out_dict = {}

	for k in from_dict:
		v = from_dict[k]

		if v in to_dict:
			out_dict[k] = to_dict[v]
			ignore.append(v)
		else:
			out_dict[k] = v

	for k in to_dict:
		if not k in ignore:
			v = to_dict[k]
			out_dict[k] = v

	for k in out_dict:
		v = out_dict[k]
		print(k, v, sep = ",")

def apply_mappings(file, mapping_dict, output_dir):
	if os.path.isdir(file):
		crawl_dir(file, mapping_dict, output_dir)
	elif file.endswith(".java"):
		remap_file(file, mapping_dict, output_dir)

def crawl_dir(target, mapping_dict, output_dir):
	print("Crawling ", target)
	files = os.listdir(target)
	for f in files:
		if target == sys.argv[2] + "/output":
			continue
		apply_mappings(target + "/" + f, mapping_dict, output_dir)

def remap_file(file, mapping_dict, output_dir):
	print("Remapping", file)
	output_filename = output_dir + file.replace(sys.argv[2], "")
	output_dir = output_filename.replace(path_leaf(output_filename), "")

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	replacements = {}

	with open(file, mode="r", encoding="utf-8") as reader:
		with open(output_filename, mode="w+", encoding="utf-8") as writer:
			for line in reader:
				if line.strip().startswith("import"):
					clazz = re.sub(r"import (.+?);", r"\1", line).strip()

					if clazz in mapping_dict:
						clazzname = re.sub(r"(?:\w+\.)+(\w+)", r"\1", clazz)
						mapped_clazzname = re.sub(r"(?:\w+\.)+(\w+)", r"\1", mapping_dict[clazz])
						if clazzname != mapped_clazzname:
							replacements[clazzname] = mapped_clazzname

						repl_line = re.sub(clazz, mapping_dict[clazz], line)
						writer.write(repl_line)
						continue

				else:
					for k in replacements:
						pattern = r"(.*\W)" + k + r"(\W.*)"
						repl = r"\1" + replacements[k] + r"\2"
						while re.search(pattern, line):
							line = re.sub(pattern, repl, line)

				writer.write(line)



def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

main()
