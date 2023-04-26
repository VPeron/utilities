#!/bin/zsh

from time import perf_counter
import os
import yara

from utils.custom_logger import get_custom_logger

"""
NOTE: run from main directory as all paths are relative from there
"""

class RuleCompiler:
    def __init__(self) -> None:
        # Compiles all rules in folder_path together
        self.folder_path = 'rules'
        self.filenames = []
        self.logger = get_custom_logger('compiler')
        self.categories = {}
    
    def make_custom_rule(self):
        pass

    def recompile_rules(self, new_filename: str):
        start = perf_counter()
        # Iterate through all files in the folder
        for filename in os.listdir(self.folder_path):
            # Check if the file is a regular file (i.e., not a folder)
            temp_file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(temp_file_path) and temp_file_path not in self.filenames:
                # collect filenames to build list of paths
                print(f'Checking: {filename}')
                self.filenames.append(temp_file_path)

        self.compiling_indexer = {str(idx+1): item for idx, item in enumerate(self.filenames)}
       
        self.rules = yara.compile(filepaths=self.compiling_indexer)
        
        self.rules.save(f'{new_filename}')
        end = perf_counter()
        self.logger.info(f"{len(self.compiling_indexer)} Rules Compiled in {end - start:.4f} seconds")

    
    def load_rules_from_file(self, file_path):
        start = perf_counter()
        self.compiled_rules = yara.load(file_path)
        print('Rules loaded')
        end = perf_counter()
        self.logger.info(f"Rules loaded from file in {end - start:.4f} seconds")
        return self.compiled_rules

session = RuleCompiler()
session.recompile_rules('compiled_rules')
