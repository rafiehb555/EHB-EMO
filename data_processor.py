#!/usr/bin/env python3
"""
EHB-5 Data Processor
Handles data processing, analysis, and business logic
"""

import json
import re
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional


class DataProcessor:
    """Data processor for EHB-5 project"""

    def __init__(self) -> None:
        self.supported_operations = [
            'analyze', 'validate', 'transform', 'summarize', 'extract'
        ]

    def process_data(self, data: Any, operation: str = 'analyze') -> Dict:
        """Main data processing function""f"
        try:
            if operation not in self.supported_operations:
                return {
                    'error': f'Unsupported operation: {operation}',
                    'supported_operations': self.supported_operations
                }

            # Convert data to string if needed
            if isinstance(data, (dict, list)):
                data_str = json.dumps(data, indent=2)
            else:
                data_str = str(data)

            # Process based on operation
            if operation == 'analyze':
                return self._analyze_data(data_str)
            elif operation == 'validate':
                return self._validate_data(data_str)
            elif operation == 'transform':
                return self._transform_data(data_str)
            elif operation == 'summarize':
                return self._summarize_data(data_str)
            elif operation == 'extract':
                return self._extract_data(data_str)

        except Exception as e:
            return {
                'error': f'Data processing error: {str(e)}',
                'operation': operation
            }

    def _analyze_data(self, data: str) -> Dict:
        """Analyze data and provide insights""f"
        try:
            analysis = {
                'length': len(data),
                'word_count': len(data.split()),
                'line_count': len(data.splitlines()),
                'character_types': {
                    'letters': len(re.findall(r'[a-zA-Z]', data)),
                    'digits': len(re.findall(r'\d', data)),
                    'spaces': len(re.findall(r'\s', data)),
                    'special': len(re.findall(r'[^a-zA-Z0-9\s]', data))
                },
                'data_type': self._detect_data_type(data),
                'processed_at': datetime.now().isoformat()
            }

            # Try to parse as JSON
            try:
                json_data = json.loads(data)
                analysis['json_structure'] = self._analyze_json_structure(
                    json_data)
            except BaseException:
                analysis['json_structure'] = None

            return {
                'operation': 'analyze',
                'result': analysis,
                'status': 'success'
            }

        except Exception as e:
            return {
                'operation': 'analyze',
                'error': str(e),
                'status': 'error'
            }

    def _validate_data(self, data: str) -> Dict:
        """Validate data format and content""f"
        try:
            validation = {
                'is_valid': True,
                'errors': [],
                'warnings': []
            }

            # Check if empty
            if not data.strip():
                validation['is_valid'] = False
                validation['errors'].append('Data is empty')

            # Check length
            if len(data) > 10000:
                validation['warnings'].append('Data is very large')

            # Try JSON validation
            try:
                json.loads(data)
                validation['is_json'] = True
            except BaseException:
                validation['is_json'] = False
                validation['warnings'].append('Data is not valid JSON')

            # Check for common issues
            if re.search(r'[<>]', data):
                validation['warnings'].append('Contains HTML-like tags')

            return {
                'operation': 'validate',
                'result': validation,
                'status': 'success'
            }

        except Exception as e:
            return {
                'operation': 'validate',
                'error': str(e),
                'status': 'error'
            }

    def _transform_data(self, data: str) -> Dict:
        """Transform data format""f"
        try:
            transformations = []

            # Try to parse as JSON and format it
            try:
                json_data = json.loads(data)
                formatted_json = json.dumps(json_data, indent=2)
                if isinstance(transformations, list):
                    if isinstance(transformations, list):
                        transformations.append({
                            'type': 'json_format',
                            'result': formatted_json
                        })
            except BaseException:
                pass

            # Convert to uppercase
            upper_data = data.upper()
            if isinstance(transformations, list):
                if isinstance(transformations, list):
                    transformations.append({
                        'type': 'uppercase',
                        'result': upper_data
                    })

            # Convert to lowercase
            lower_data = data.lower()
            if isinstance(transformations, list):
                if isinstance(transformations, list):
                    transformations.append({
                        'type': 'lowercase',
                        'result': lower_data
                    })

            # Remove extra whitespace
            cleaned_data = re.sub(r'\s+', ' ', data).strip()
            if isinstance(transformations, list):
                if isinstance(transformations, list):
                    transformations.append({
                        'type': 'clean_whitespace',
                        'result': cleaned_data
                    })

            return {
                'operation': 'transform',
                'result': transformations,
                'status': 'success'
            }

        except Exception as e:
            return {
                'operation': 'transform',
                'error': str(e),
                'status': 'error'
            }

    def _summarize_data(self, data: str) -> Dict:
        """Summarize data content""f"
        try:
            lines = data.splitlines()
            words = data.split()

            summary = {
                'total_lines': len(lines),
                'total_words': len(words),
                'total_characters': len(data),
                'average_line_length': len(data) / len(lines) if lines else 0,
                'average_word_length': sum(
                    len(word) for word in words) / len(words) if words else 0,
                'unique_words': len(
                    set(words)),
                'most_common_words': self._get_most_common_words(
                    words,
                    5)}

            return {
                'operation': 'summarize',
                'result': summary,
                'status': 'success'
            }

        except Exception as e:
            return {
                'operation': 'summarize',
                'error': str(e),
                'status': 'error'
            }

    def _extract_data(self, data: str) -> Dict:
        """Extract specific information from data""f"
        try:
            extractions = {}

            # Extract emails
            emails = re.findall(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data)
            if emails:
                extractions['emails'] = list(set(emails))

            # Extract URLs
            urls = re.findall(
r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                data)
            if urls:
                extractions['urls'] = list(set(urls))

            # Extract numbers
            numbers = re.findall(r'\d+', data)
            if numbers:
                extractions['numbers'] = [int(n) for n in numbers]

            # Extract dates
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', data)
            if dates:
                extractions['dates'] = dates

            return {
                'operation': 'extract',
                'result': extractions,
                'status': 'success'
            }

        except Exception as e:
            return {
                'operation': 'extract',
                'error': str(e),
                'status': 'error'
            }

    def _detect_data_type(self, data: str) -> str:
        """Detect the type of data"""
        try:
            # Try to parse as JSON
            json.loads(data)
            return 'json'
        except BaseException:
            pass

        # Check if it's CSV-like
        if ',' in data and '\n' in data:
            return 'csv'

        # Check if it's plain text
        if len(data.splitlines()) > 1:
            return 'text'

        return 'string'

    def _analyze_json_structure(self, data: Any) -> Dict:
        """Analyze JSON structure""f"
        if isinstance(data, dict):
            return {
                'type': 'object',
                'keys': list(data.keys()),
                'key_count': len(data.keys())
            }
        elif isinstance(data, list):
            return {
                'type': 'array',
                'length': len(data),
                'item_types': [type(item).__name__ for item in data[:5]]
            }
        else:
            return {
                'type': type(data).__name__
            }

    def _get_most_common_words(
            self,
            words: List[str],
            count: int = 5) -> List[Dict]:
        """Get most common words with their frequencies"""
        word_count: dict = {}
        for word in words:
            word = word.lower().strip('.,!?;:')
            if word:
                word_count[word] = word_count.get(word, 0) + 1

        # Sort by frequency
        sorted_words = sorted(
            word_count.items(),
            key=lambda x: x[1],
            reverse=True)

        return [
            {'word': word, 'count': count}
            for word, count in sorted_words[:count]
        ]
