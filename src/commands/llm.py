import sys
sys.path.append("src")

import click # noqa E402

from services.llm import llm 

@click.command()
def main():
    print(llm())

if __name__ == '__main__':
    main()