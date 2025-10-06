"""
Movers Analyzer Module
Identifies and ranks the biggest odds movers
"""
import pandas as pd
from typing import List, Dict


class MoversAnalyzer:
    """Analyze odds data to identify biggest movers"""

    def __init__(self, df: pd.DataFrame, config: Dict):
        """
        Initialize analyzer with dataframe and configuration

        Args:
            df: DataFrame with odds data
            config: Configuration dict with thresholds
        """
        self.df = df.copy()
        self.config = config
        self.movers = None

    def identify_movers(self) -> pd.DataFrame:
        """
        Identify significant movers based on threshold

        Returns:
            DataFrame of movers sorted by absolute change
        """
        threshold = self.config.get('movement_threshold', 2.0)

        # Filter by threshold
        self.df['abs_change'] = self.df['change_pct'].abs()
        movers = self.df[self.df['abs_change'] >= threshold].copy()

        # Sort by absolute change (descending)
        movers = movers.sort_values('abs_change', ascending=False)

        # Limit to top N
        top_n = self.config.get('top_n_movers', 10)
        movers = movers.head(top_n)

        # Add categorization
        movers['direction'] = movers['change_pct'].apply(
            lambda x: 'up' if x > 0 else 'down'
        )

        movers['category'] = movers['direction'].map({
            'up': 'riser',
            'down': 'faller'
        })

        # Add magnitude classification
        movers['magnitude'] = movers['abs_change'].apply(self._classify_magnitude)

        self.movers = movers
        return movers

    def _classify_magnitude(self, change: float) -> str:
        """
        Classify magnitude of change

        Args:
            change: Absolute percentage change

        Returns:
            Magnitude classification
        """
        if change >= 10:
            return 'massive'
        elif change >= 5:
            return 'significant'
        elif change >= 3:
            return 'notable'
        else:
            return 'moderate'

    def get_movers_by_market(self, market: str) -> pd.DataFrame:
        """
        Get movers filtered by market type

        Args:
            market: Market name to filter by

        Returns:
            Filtered DataFrame
        """
        if self.movers is None:
            self.identify_movers()

        return self.movers[self.movers['market'] == market]

    def get_top_risers(self, n: int = 5) -> pd.DataFrame:
        """
        Get top N risers

        Args:
            n: Number of risers to return

        Returns:
            DataFrame of top risers
        """
        if self.movers is None:
            self.identify_movers()

        risers = self.movers[self.movers['direction'] == 'up']
        return risers.head(n)

    def get_top_fallers(self, n: int = 5) -> pd.DataFrame:
        """
        Get top N fallers

        Args:
            n: Number of fallers to return

        Returns:
            DataFrame of top fallers
        """
        if self.movers is None:
            self.identify_movers()

        fallers = self.movers[self.movers['direction'] == 'down']
        return fallers.head(n)

    def get_movers_summary(self) -> Dict:
        """
        Get summary statistics of movers

        Returns:
            Dictionary with summary stats
        """
        if self.movers is None:
            self.identify_movers()

        return {
            'total_movers': len(self.movers),
            'risers_count': len(self.movers[self.movers['direction'] == 'up']),
            'fallers_count': len(self.movers[self.movers['direction'] == 'down']),
            'avg_change': round(self.movers['change_pct'].mean(), 2),
            'biggest_riser': self._format_biggest_mover(self.get_top_risers(1)),
            'biggest_faller': self._format_biggest_mover(self.get_top_fallers(1)),
            'markets_affected': self.movers['market'].unique().tolist()
        }

    def _format_biggest_mover(self, df: pd.DataFrame) -> Dict:
        """Format biggest mover info"""
        if df.empty:
            return {}

        row = df.iloc[0]
        return {
            'market': row['market'],
            'team_player': row['team_player'],
            'change_pct': round(row['change_pct'], 2)
        }

    def to_dict_list(self) -> List[Dict]:
        """
        Convert movers to list of dictionaries for JSON export

        Returns:
            List of mover dictionaries
        """
        if self.movers is None:
            self.identify_movers()

        return self.movers.to_dict('records')
