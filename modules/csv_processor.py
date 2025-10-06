"""
CSV Processor Module
Handles importing, validating, and parsing NFL futures odds CSV data
"""
import pandas as pd
from typing import Dict, List, Optional


class CSVProcessor:
    """Process and validate NFL futures odds CSV files"""

    # Column mapping: support multiple CSV formats
    COLUMN_MAPPING = {
        # Standard format (lowercase)
        'market': 'market',
        'team_player': 'team_player',
        'last_week_pct': 'last_week_pct',
        'this_week_pct': 'this_week_pct',
        'change_pct': 'change_pct',
        'last_week_american': 'last_week_american',
        'this_week_american': 'this_week_american',

        # Alternative format (capitalized with spaces)
        'Market': 'market',
        'Team/Player': 'team_player',
        'Last Week Percent Odds': 'last_week_pct',
        'This Week Percent Odds': 'this_week_pct',
        'Change in % Odds (WoW)': 'change_pct',
        'Last Week American Odds': 'last_week_american',
        'This Week American Odds': 'this_week_american',
    }

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

    def normalize_columns(self) -> bool:
        """Normalize column names to standard format"""
        if self.df is None:
            return False

        # Rename columns based on mapping
        rename_dict = {}
        for col in self.df.columns:
            if col in self.COLUMN_MAPPING:
                rename_dict[col] = self.COLUMN_MAPPING[col]

        if rename_dict:
            self.df = self.df.rename(columns=rename_dict)

        return True

    def validate_structure(self) -> bool:
        """Validate that CSV has required columns"""
        if self.df is None:
            self.validation_errors.append("No data loaded")
            return False

        # Check which columns are present after normalization
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]

        if missing_columns:
            available = list(self.df.columns)
            self.validation_errors.append(
                f"Missing required columns: {', '.join(missing_columns)}. "
                f"Available columns: {', '.join(available)}"
            )
            return False

        return True

    def clean_data(self) -> None:
        """Clean and format data"""
        if self.df is None:
            return

        # Convert percentage columns to float (remove % sign if present)
        pct_columns = ['last_week_pct', 'this_week_pct', 'change_pct']
        for col in pct_columns:
            if col in self.df.columns:
                # Remove % sign and convert to numeric
                self.df[col] = self.df[col].astype(str).str.replace('%', '').str.replace('+', '')
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Convert American odds to int
        american_columns = ['last_week_american', 'this_week_american']
        for col in american_columns:
            if col in self.df.columns:
                # Remove + sign if present
                self.df[col] = self.df[col].astype(str).str.replace('+', '')
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Strip whitespace from string columns and clean team names
        if 'market' in self.df.columns:
            self.df['market'] = self.df['market'].str.strip()

        if 'team_player' in self.df.columns:
            self.df['team_player'] = self.df['team_player'].str.strip()
            # Remove the suffix like "TO_MAKE_THE_PLAYOFFS" from team names
            self.df['team_player'] = self.df['team_player'].str.replace(r'\s+TO_MAKE_THE_PLAYOFFS$', '', regex=True)
            self.df['team_player'] = self.df['team_player'].str.replace(r'\s+MVP$', '', regex=True)

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

        # Normalize column names before validation
        self.normalize_columns()

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
