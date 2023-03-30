import lzma


def compress(input_file, output_file):
    with open(input_file, 'rb') as src, lzma.open(output_file, 'wb') as dest:
        dest.writelines(src)


def decompress(input_file, output_file):
    with lzma.open(input_file, 'rb') as src, open(output_file, 'wb') as dest:
        dest.writelines(src)

