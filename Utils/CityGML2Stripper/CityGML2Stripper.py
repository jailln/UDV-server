import argparse
import lxml.etree as ET

def ParseCommandLine():
    # arg parse
    descr = '''A small utility that strips a CityGML 2.0 (XML) 
            files and serialize the result in a new CityGML (XML) 
            file. It removes appearences and generic attributes.'''
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('--input',
                        nargs='+',
                        type=str,
                        help='CityGML input file')
    parser.add_argument('--output',
                        nargs='+',
                        default='output.gml',
                        type=str,
                        help='Resulting file.')
    return parser.parse_args()

if __name__ == '__main__':
    cli_args = ParseCommandLine()
    filename = cli_args.input[0]

    # parse file
    parser = ET.XMLParser(remove_comments=True)
    parsed_file = ET.parse(filename, parser)

    # Refer to this doc for more information: https://lxml.de/api/index.html
    # in submodule lxml.etree, function strip_elements
    # Remove all elements in the namespace app
    ET.strip_elements(parsed_file,
                      '{' + parsed_file.getroot().nsmap['app'] + '}' + '*')
    # Remove all generic attributes
    ET.strip_elements(parsed_file,
                      '{' + parsed_file.getroot().nsmap['gen'] + '}' + '*')

    parsed_file.write(cli_args.output[0])
