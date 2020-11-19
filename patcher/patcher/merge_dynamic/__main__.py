import argparse
import sys

from .log import set_verbose
from .merge_dynamic import merge_dynamic

parser = argparse.ArgumentParser(
    description="Merge the dynamic portions of the translate ELF with the one from the host ELF."
)
parser.add_argument(
    "to_extend",
    metavar="TO_EXTEND",
    help="The ELF to extend.",
)
parser.add_argument(
    "source",
    metavar="SOURCE",
    help="The original ELF.",
)
parser.add_argument(
    "output",
    metavar="OUTPUT",
    nargs="?",
    default="-",
    help="The output ELF.",
)
parser.add_argument(
    "--verbose",
    action="store_true",
    help="Print debug information and warnings.",
)
parser.add_argument(
    "--base",
    metavar="ADDRESS",
    default="0x50000000",
    help="The base address where dynamic object have been loaded.",
)
parser.add_argument(
    "--merge-load-segments",
    action="store_true",
    help="Merge the LOADed segments from the source ELF into the output ELF."
)

if __name__ == "__main__":
    args = parser.parse_args()
    set_verbose(args.verbose)

    with sys.stdout if args.output == "-" else open(args.output, "wb") as output_file, \
            open(args.source, "rb") as source_file, \
            open(args.to_extend, "rb") as to_extend_file:
        base = int(args.base, base=0)
        retcode = merge_dynamic(
            to_extend_file,
            source_file,
            output_file,
            base=base,
            merge_load_segments=args.merge_load_segments,
        )

    sys.exit(retcode)
