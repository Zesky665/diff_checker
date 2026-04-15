import zipfile
from io import BytesIO
from typing import Dict, Set
import os
import hashlib

def get_zip_structure(zip_file) -> Dict[str, Set[str]]:
    """Extract directory structure from zip file"""
    structure = {'dirs': set(), 'files': set()}
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for name in zip_ref.namelist():
            if name.endswith('/'):
                structure['dirs'].add(name.rstrip('/'))
            else:
                structure['files'].add(name)
                path_parts = os.path.dirname(name).split('/')
                for i in range(len(path_parts)):
                    parent_dir = '/'.join(path_parts[:i+1])
                    if parent_dir:
                        structure['dirs'].add(parent_dir)
    return structure

def get_file_hash(zip_file, file_path) -> str:
    """Calculate SHA256 hash of a file within a zip archive"""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        with zip_ref.open(file_path) as file:
            return hashlib.sha256(file.read()).hexdigest()

def compare_file_contents(zip1, zip2, common_files) -> Dict[str, Set[str]]:
    """Compare contents of files that exist in both zip files"""
    identical_files = set()
    different_files = set()

    with zipfile.ZipFile(zip1, 'r') as zip1_ref, \
         zipfile.ZipFile(zip2, 'r') as zip2_ref:

        for file_path in common_files:
            try:
                with zip1_ref.open(file_path) as file1, \
                     zip2_ref.open(file_path) as file2:

                    hash1 = hashlib.sha256(file1.read()).hexdigest()
                    hash2 = hashlib.sha256(file2.read()).hexdigest()

                    if hash1 == hash2:
                        identical_files.add(file_path)
                    else:
                        different_files.add(file_path)
            except Exception:
                # If we can't read the file, mark it as different
                different_files.add(file_path)

    return {
        'identical': identical_files,
        'different': different_files
    }

def compare_zips(zip1, zip2) -> Dict:
    """Compare two zip files and return differences"""
    struct1 = get_zip_structure(zip1)
    struct2 = get_zip_structure(zip2)

    files_only_in_1 = struct1['files'] - struct2['files']
    files_only_in_2 = struct2['files'] - struct1['files']
    common_files = struct1['files'] & struct2['files']

    dirs_only_in_1 = struct1['dirs'] - struct2['dirs']
    dirs_only_in_2 = struct2['dirs'] - struct1['dirs']

    # Compare contents of common files
    content_comparison = compare_file_contents(zip1, zip2, common_files)

    return {
        'zip1_total_files': len(struct1['files']),
        'zip1_total_dirs': len(struct1['dirs']),
        'zip2_total_files': len(struct2['files']),
        'zip2_total_dirs': len(struct2['dirs']),
        'files_only_in_zip1': sorted(files_only_in_1),
        'files_only_in_zip2': sorted(files_only_in_2),
        'dirs_only_in_zip1': sorted(dirs_only_in_1),
        'dirs_only_in_zip2': sorted(dirs_only_in_2),
        'common_files': sorted(common_files),
        'common_dirs': sorted(struct1['dirs'] & struct2['dirs']),
        'files_with_identical_content': sorted(content_comparison['identical']),
        'files_with_different_content': sorted(content_comparison['different'])
    }
