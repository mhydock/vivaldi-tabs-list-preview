import argparse, os, re, sys

from shutil import copy
from xml.dom import minidom
from xml.etree import ElementTree

def patch_browser_html(inst_dir):
    browser_file = os.path.join(inst_dir, 'browser.html')
    copy(browser_file, browser_file + '.bak')

    browser = ElementTree.parse(browser_file)

    body = browser.find('.//body')
    has_jqr = browser.findall('.//*[@src="jquery-3.2.0.min.js"]')
    has_tpl = browser.findall('.//*[@src="tab-preview-list.js"]')

    if not has_jqr:
        ElementTree.SubElement(body, 'script', {'src': 'jquery-3.2.0.min.js'})

    if not has_tpl:
        ElementTree.SubElement(body, 'script', {'src': 'tab-preview-list.js'})

    rough_string = ElementTree.tostring(browser.getroot(), encoding='unicode')
    rough_string = re.sub(r'(\>)(\s*)(\<)', r'\1\3', rough_string)
    print(rough_string)
    pretty_string = minidom.parseString(rough_string).toprettyxml(indent="  ")
    pretty_string = re.sub(r'(\<script)(.*?)(/\>)', r'\1\2></script>', pretty_string)
    pretty_string = pretty_string.replace('<?xml version="1.0" ?>', '<!DOCTYPE html>')
    print(pretty_string)

    with open(browser_file, 'w') as browser_html:
        browser_html.write(pretty_string)


def patch_common_css(inst_dir):
    css_file = os.path.join(inst_dir, 'style', 'common.css')
    copy(css_file, css_file + '.bak')
    with open(css_file, 'r', encoding='utf-8') as css:
        lines = css.readlines()

    res = filter(lambda x: '@import "tab-preview-list.css";' in x, lines)
    if not list(res):
        with open(css_file, 'w', encoding='utf-8') as css:
            css.write('@import "tab-preview-list.css";\n\n')
            for line in lines:
                css.write(line)


def main(argv):
    parser = argparse.ArgumentParser(description='Patches given Vivaldi installation with customizations in this directory.')
    parser.add_argument('path', help='The full path of the Vivaldi installation to patch')

    args = parser.parse_args(argv)
    path = os.path.expanduser(args.path)

    if not path:
        parser.print_usage()
        return 1

    if not os.path.exists(path):
        print('Given path does not exist')
        return 1

    if not os.path.isdir(path):
        print('Given path is not a directory')
        return 1

    reg = re.compile(r'[0-9]+\.[0-9]+\.*')
    inst = [dir for dir in os.listdir(path) if reg.match(dir)]

    if not inst:
        print('No Vivaldi installations found in given directory')
        return 1

    inst_dir = os.path.join(path, inst[-1], 'resources', 'vivaldi')

    copy('./jquery-3.2.0.min.js', inst_dir)
    copy('./tab-preview-list.js', inst_dir)
    copy('./tab-preview-list.css', os.path.join(inst_dir, 'style'))
    
    patch_browser_html(inst_dir)
    patch_common_css(inst_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
