import os
import shutil
import subprocess
import glob

def merge_fastq_files(directory_path, output_file_name):
    # Define the allowed file extensions for FASTQ files
    allowed_extensions = ['.fastq', '.fq', '.fastq.gz', '.fq.gz']

    # Initialize lists for gzipped and non-gzipped files
    gzipped_files = []
    non_gzipped_files = []

    # Get a list of all files in the directory
    all_files = glob.glob(os.path.join(directory_path, '*'))

    print("Scanning for FASTQ files in directory:", directory_path)

    # Filter files based on allowed extensions
    for file in all_files:
        if any(file.endswith(extension) for extension in allowed_extensions):
            if file.endswith('.gz'):
                gzipped_files.append(file)
                print(f"Found gzipped FASTQ file: {file}")
            else:
                non_gzipped_files.append(file)
                print(f"Found non-gzipped FASTQ file: {file}")

    # Check if both gzipped and non-gzipped files are found
    if gzipped_files and non_gzipped_files:
        print("Both gzipped and non-gzipped FASTQ files found. Only gzipped files will be merged.")

    # Define default output directory
    default_output_directory = '/var/lib/cge/data'

    # Use home directory as a fallback
    fallback_output_directory = os.path.expanduser('~')

    # Determine the output directory based on existence
    output_directory = default_output_directory if os.path.exists(default_output_directory) else fallback_output_directory

    print(f"Output directory set to: {output_directory}")

    # Merge gzipped files into one if they exist
    if gzipped_files:
        print("Merging gzipped files...")
        merged_gzipped_file_path = os.path.join(output_directory, output_file_name + '.fastq.gz')
        with open(merged_gzipped_file_path, 'wb') as output:
            for gzipped_file in gzipped_files:
                print(f"Adding {gzipped_file} to merged file.")
                with open(gzipped_file, 'rb') as input_file:
                    shutil.copyfileobj(input_file, output)

        print(f"Merged gzipped file saved at: {merged_gzipped_file_path}")

    # If only non-gzipped files are found, merge and gzip them
    elif non_gzipped_files:
        print("Merging and gzipping non-gzipped files...")
        merged_non_gzipped_file_path = os.path.join(output_directory, output_file_name + '.fastq')

        # Concatenate the non-gzipped files into one
        cat_command = 'cat {} > {}'.format(' '.join(non_gzipped_files), merged_non_gzipped_file_path)
        subprocess.run(cat_command, shell=True)

        # Gzip the merged file
        gzip_command = 'gzip -f {}'.format(merged_non_gzipped_file_path)
        subprocess.run(gzip_command, shell=True)

        # Rename the gzipped file to ensure it ends with '.fastq.gz'
        os.rename(merged_non_gzipped_file_path + '.gz', merged_non_gzipped_file_path + '.fastq.gz')

        print(f"Merged non-gzipped file saved at: {merged_non_gzipped_file_path}.fastq.gz")

# Example usage
# merge_fastq_files('/path/to/directory', 'output_file_name')
