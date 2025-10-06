"""
CSV Processor Module
Handles importing, validating, and parsing NFL futures odds CSV data
"""
import pandas as pd
from typing import Dict, List, Optional


class CSVProcessor:
    """Process and validate NFL futures odds CSV files"""

    REQUIRED_COLUMNS = [
        'market',
        'team_player',
        'last_week_pct',
        'this_week_pct',
        'change_pct',
        'last_week_american',
        'this_week_american'
    ]

    def __init__(self, file_path: str = None, file_object=None):
        """
        Initialize processor with CSV file path or file object

        Args:
            file_path: Path to CSV file (for local files)
            file_object: File-like object (for uploads in serverless environments)
        """
        self.file_path = file_path
        self.file_object = file_object
        self.df = None
        self.validation_errors = []

    def load_csv(self) -> bool:
        """Load CSV file into dataframe from path or file object"""
        try:
            if self.file_object is not None:
                # Process from file object (uploaded file)
                self.df = pd.read_csv(self.file_object)
            elif self.file_path is not None:
                # Process from file path (local file)
                self.df = pd.read_csv(self.file_path)
            else:
                self.validation_errors.append("No file path or file object provided")
                return False
            return True
        except Exception as e:
            self.validation_errors.append(f"Failed to load CSV: {str(e)}")
            return False

    def validate_structure(self) -> bool:
        """Validate that CSV has required columns"""
        if self.df is None:
            self.validation_errors.append("No data loaded")
            return False

        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]

        if missing_columns:
            self.validation_errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return False

        return True

    def clean_data(self) -> None:
        """Clean and format data"""
        if self.df is None:
            return

        # Convert percentage columns to float
        pct_columns = ['last_week_pct', 'this_week_pct', 'change_pct']
        for col in pct_columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Convert American odds to int
        american_columns = ['last_week_american', 'this_week_american']
        for col in american_columns:
            # Remove + sign if present
            self.df[col] = self.df[col].astype(str).str.replace('+', '')
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Strip whitespace from string columns
        self.df['market'] = self.df['market'].str.strip()
        self.df['team_player'] = self.df['team_player'].str.strip()

        # Handle missing values
        self.df = self.df.dropna(subset=['market', 'team_player', 'change_pct'])

    def get_data(self) -> Optional[pd.DataFrame]:
        """Get processed dataframe"""
        return self.df

    def get_errors(self) -> List[str]:
        """Get validation errors"""
        return self.validation_errors

    def process(self) -> bool:
        """Run full processing pipeline"""
        if not self.load_csv():
            return False

        if not self.validate_structure():
            return False

        self.clean_data()
        return True

    def get_summary(self) -> Dict:
        """Get summary statistics of loaded data"""
        if self.df is None:
            return {}

        return {
            'total_rows': len(self.df),
            'markets': self.df['market'].unique().tolist(),
            'market_counts': self.df['market'].value_counts().to_dict(),
            'avg_change': round(self.df['change_pct'].mean(), 2),
            'max_change': round(self.df['change_pct'].max(), 2),
            'min_change': round(self.df['change_pct'].min(), 2)
        }
