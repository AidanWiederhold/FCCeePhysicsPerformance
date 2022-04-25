def run(input_file, output_file):
    import uproot
    from bdt_config import train_vars_vtx, loc
    inf = uproot.open(input_file)
    tree = inf['events']
    vars_list = train_vars_vtx.copy()
    df = tree.arrays(library="pd", how="zip", filter_name=train_vars_vtx)
    df.to_pickle(output_file)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, required=True, help='Select the input file(s).')
    parser.add_argument('--output', type=str, required=True, help='Select the output file.')
    args = parser.parse_args()

    run(args.input, args.output)

if __name__ == '__main__':
    main()