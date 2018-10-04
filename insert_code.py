"""
insert_code.py - insert code into slides

Terry Brown, terrynbrown@gmail.com, Thu Oct  4 16:32:38 2018
"""

import argparse

def make_parser():

    parser = argparse.ArgumentParser(
        description="""insert code into slides""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--markdown",
        help="Markdown file to process"
    )
    parser.add_argument("--code-slide", nargs=2, action='append',
        metavar=('PYFILE', 'SLIDE'), default=[],
        help="Markdown file to process"
    )

    return parser

def get_options(args=None):
    """
    get_options - use argparse to parse args, and return a
    argparse.Namespace, possibly with some changes / expansions /
    validatations.

    Client code should call this method with args as per sys.argv[1:],
    rather than calling make_parser() directly.

    :param [str] args: arguments to parse
    :return: options with modifications / validations
    :rtype: argparse.Namespace
    """
    opt = make_parser().parse_args(args)

    # modifications / validations go here

    return opt

def insert(text, code, slide):
    lines = text.split('\n')
    new_lines = []
    placed = False

    while lines:
        line = lines.pop(0)
        if not placed and line.startswith('#') and line.endswith(slide):
            placed = True
            while not line.startswith('```'):
                # copy to opening ``` line
                new_lines.append(line)
                line = lines.pop(0)
            new_lines.append(line)  # copy opening ``` line
            code = open(code).read().strip()
            while "\n\n\n" in code:
                code = code.replace("\n\n\n", "\n\n")
            new_lines.append(code)
            while not line.endswith('```'):
                # drop old code
                line = lines.pop(0)
            new_lines.append(line)  # copy closing ``` line
        else:
            new_lines.append(line)

    return '\n'.join(new_lines)

def main():

    opt = get_options()

    text = open(opt.markdown).read()

    for code, slide in opt.code_slide:
        text = insert(text, code, slide)

    print(text, end='')

if __name__ == '__main__':
    main()
