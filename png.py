import os
import subprocess

def convert_svg_to_png(svg_file, png_file):
    subprocess.run(['inkscape', svg_file, '--export-filename', png_file], check=True)

def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.svg'):
                svg_file = os.path.join(root, file)
                relative_path = os.path.relpath(svg_file, input_dir)
                png_file = os.path.join(output_dir, relative_path)
                png_file = png_file.replace('.svg', '.png')

                os.makedirs(os.path.dirname(png_file), exist_ok=True)
                convert_svg_to_png(svg_file, png_file)

if __name__ == '__main__':
    input_directory = 'figures'
    output_directory = 'png'
    process_directory(input_directory, output_directory)
