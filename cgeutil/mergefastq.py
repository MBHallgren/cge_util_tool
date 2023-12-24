import os
import glob
import subprocess
import shutil

def merge_fastq_files(directory_path, output_file_name):
    # Define the allowed file extensions for FASTQ files
    allowed_extensions = ['.fastq', '.fq', '.fastq.gz', '.fq.gz']

    # Initialize lists for gzipped and non-gzipped files
    gzipped_files = []
    non_gzipped_files = []

    # Get a list of all files in the directory
    all_files = glob.glob(os.path.join(directory_path, '*'))

    # Filter files based on allowed extensions
    for file in all_files:
        if any(file.endswith(extension) for extension in allowed_extensions):
            if file.endswith('.gz'):
                gzipped_files.append(file)
            else:
                non_gzipped_files.append(file)

    # Check if both gzipped and non-gzipped files are found
    if gzipped_files and non_gzipped_files:
        print ("Both gzipped and non-gzipped FASTQ files found.")
        print ("Only the gzipped files will be merged.")

    # Merge gzipped files into one if they exist
    if gzipped_files:
        merged_gzipped_file = os.path.join(directory_path, output_file_name)
        with open(merged_gzipped_file, 'wb') as output:
            for gzipped_file in gzipped_files:
                with open(gzipped_file, 'rb') as input_file:
                    shutil.copyfileobj(input_file, output)

    # If only non-gzipped files are found, merge and gzip them
    elif non_gzipped_files:
        merged_non_gzipped_file = os.path.join(directory_path, output_file_name + '.fastq.gz')
        cat_command = 'cat {} | gzip > {}'.format(' '.join(non_gzipped_files), merged_non_gzipped_file)
        subprocess.run(cat_command, shell=True)

    # Move the merged file to the specified directory
    output_directory = '/var/lib/cge/data'
    merged_output_path = os.path.join(output_directory, output_file_name)
    shutil.move(merged_gzipped_file, merged_output_path)
    print("Merged FASTQ file saved at:", merged_output_path)

# Example usage:
# merge_fastq_files('/path/to/directory', 'merged_output.fastq')
