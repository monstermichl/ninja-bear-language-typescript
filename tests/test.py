from os import path
import os
import pathlib
import re
import shutil
from typing import List
import unittest

from ninja_bear import Orchestrator, LanguageConfigBase


_NINJA_BEAR_REFERENCE_REGEX = r'Generated with ninja-bear v\d+\.\d+\.\d+'


class Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._test_path = pathlib.Path(__file__).parent.resolve()
        self._test_config_path = path.join(self._test_path, '..', 'example/test-config.yaml')
        self._test_compare_files_path = path.join(self._test_path, 'compare_files')

    def test_read_config(self):
        orchestrator = Orchestrator.read_config(self._test_config_path)
        self._evaluate_configs(orchestrator.language_configs)

    def test_parse_config(self):
        TEST_INCLUDE = 'test-include.yaml'

        with open(self._test_config_path, 'r') as f:
            content = f.read().replace(TEST_INCLUDE, os.path.join(os.getcwd(), 'example', TEST_INCLUDE))
        orchestrator = Orchestrator.parse_config(content, 'test-config')
        self._evaluate_configs(orchestrator.language_configs)

    def test_run_generators(self):
        orchestrator = Orchestrator.read_config(self._test_config_path)

        for config in orchestrator.language_configs:
            compare_file_path = path.join(
                self._test_compare_files_path,
                f'{config.config_info.file_name_full}'
            )
            
            with open(compare_file_path, 'r') as f:
                content = f.read()

            original_max_diff = self.maxDiff
            self.maxDiff = None
            self.assertEqual(
                # Remove versions to keep tests working if version changed.
                re.sub(_NINJA_BEAR_REFERENCE_REGEX, '', config.dump()), 
                re.sub(_NINJA_BEAR_REFERENCE_REGEX, '', content),
            )
            self.maxDiff = original_max_diff

    def test_write_configs(self):
        OUTPUT_DIR = path.join(self._test_path, 'test_output')
        orchestrator = Orchestrator.read_config(self._test_config_path)

        if not os.path.isdir(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        
        # Write all configs to the output folder.
        orchestrator.write(OUTPUT_DIR)

        # Collect the output file names.
        files = os.listdir(OUTPUT_DIR)

        # Cleanup output directory.
        shutil.rmtree(OUTPUT_DIR)

        # Compare files.
        for config in orchestrator.language_configs:
            self.assertIn(config.config_info.file_name_full, files)

    def _evaluate_configs(self, configs: List[LanguageConfigBase]):
        checks = [
            # Check TypeScript config.
            ['ts', 'test_config'],
        ]

        self.assertIsNotNone(configs)
        self.assertIsInstance(configs, list)
        self.assertEqual(len(configs), len(checks))

        # Check the languages.
        for i, check in enumerate(checks):
            self._evaluate_common_properties(configs[i], check[0], check[1])

    def _evaluate_common_properties(
        self,
        config: LanguageConfigBase,
        extension: str,
        name: str,
    ):
        self.assertEqual(config.config_info.file_extension, extension)
        self.assertEqual(config.config_info.file_name, name)
