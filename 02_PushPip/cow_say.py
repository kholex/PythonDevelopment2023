import sys
import argparse
from cowsay import cowsay, list_cows
from os import getcwd

parser = argparse.ArgumentParser()
parser.add_argument('-e', dest='e', default='oo', help='Selects the appearance of the cow’s eyes, in which case the first two characters of the argument string eye_string will be used. The default eyes are oo.', type=str)
parser.add_argument('-f', dest='f', default='default', help='Specifies a particular cow picture file (cowfile) to use. If the cowfile spec resolves to an existing file, then it will be interpreted as a path to the cowfile.', type=str)
parser.add_argument('-T', dest='T', default='  ', help='Custom tongue string.', action='store')
parser.add_argument('-W', dest='W', help='Specifies roughly where the message should be wrapped', type=int)
parser.add_argument('-b', dest='b', help='Invokes Borg mode.', action='store_true')
parser.add_argument('-d', dest='d', help='Causes the cow to appear dead.', action='store_true')
parser.add_argument('-g', dest='g', help='Invokes greedy mode.', action='store_true')
parser.add_argument('-l', help='Lists the defined cows on the current COWPATH. Displays it in a human-readable pretty-printed format when displaying to a terminal device.', action='store_true')
parser.add_argument('-n', dest='n', help='Whether text should be wrapped in the bubble.', action='store_true')
parser.add_argument('-p', dest='p', help='Causes a state of paranoia to come over the cow.', action='store_true')
parser.add_argument('-s', dest='s', help='Makes the cow appear thoroughly stoned.', action='store_true')
parser.add_argument('-t', dest='t', help='Yields a tired cow.', action='store_true')
parser.add_argument('-w', dest='w', help='Is somewhat the opposite of -t, and initiates wired mode.', action='store_true')
parser.add_argument('-y', dest='y', help='Brings on the cow’s youthful appearance.', action='store_true')
parser.add_argument('message', help='A string to wrap in the text bubble.', default=" ", nargs="?")

args = parser.parse_args()

if args.l:
    print(list_cows())
else:
    preset = [p for p in "bdgpstwy" if args.__dict__[p]]
    cow = 'default' if ('/' in args.f) else args.f
    cowfile = args.f if ('/' in args.f) else None

    if '/' in args.message:
        with open(args.message, "r") as f:
            args.message = f.read()

    print(cowsay(
        message=args.message,
        cow=cow,
        preset=preset[0] if preset else None,
        eyes=args.e[:2],
        tongue=args.T[:2],
		wrap_text=args.n,
        width=args.W,
        cowfile=cowfile
    ))
