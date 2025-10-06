"""
Tweet Generator Module
Generates tweet content using templates and mover data
"""
from typing import Dict, List
import pandas as pd
from .templates import TweetTemplates


class TweetGenerator:
    """Generate tweet drafts for odds movers"""

    def __init__(self, config: Dict):
        """
        Initialize generator with configuration

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.include_emojis = config.get('include_emojis', True)
        self.character_limit = config.get('character_limit', 280)
        self.tweet_variations = config.get('tweet_variations', 2)

    def generate_for_mover(self, mover: Dict, context: str = None) -> Dict:
        """
        Generate tweet drafts for a single mover

        Args:
            mover: Dictionary with mover data
            context: Optional context string to include

        Returns:
            Dictionary with mover info and tweet drafts
        """
        # Extract mover data
        market = mover['market']
        team_player = mover['team_player']
        direction = mover['category']  # 'riser' or 'faller'
        change_pct = mover['change_pct']
        magnitude = mover['magnitude']

        # Format odds
        last_odds = self._format_american_odds(mover['last_week_american'])
        this_odds = self._format_american_odds(mover['this_week_american'])

        # Get templates
        templates = TweetTemplates.get_templates(market, direction)

        # Limit to configured number of variations
        templates = templates[:self.tweet_variations]

        # Generate context
        if context is None:
            context = self._generate_placeholder_context(mover)

        # Generate tweet variations
        tweet_drafts = []
        for template_data in templates:
            tweet_content = self._fill_template(
                template_data['template'],
                mover=mover,
                market=market,
                team_player=team_player,
                last_odds=last_odds,
                this_odds=this_odds,
                change=change_pct,
                context=context
            )

            # Count characters
            char_count = len(tweet_content)

            # Check if over limit
            within_limit = char_count <= self.character_limit

            tweet_drafts.append({
                'version': template_data['name'],
                'content': tweet_content,
                'character_count': char_count,
                'within_limit': within_limit
            })

        # Build result
        result = {
            'market': market,
            'team_player': team_player,
            'movement': {
                'last_week_pct': round(mover['last_week_pct'], 2),
                'this_week_pct': round(mover['this_week_pct'], 2),
                'change_pct': round(change_pct, 2),
                'direction': mover['direction'],
                'magnitude': magnitude,
                'last_week_american': last_odds,
                'this_week_american': this_odds
            },
            'context_used': context,
            'tweet_drafts': tweet_drafts
        }

        return result

    def generate_batch(self, movers: pd.DataFrame, contexts: Dict = None) -> List[Dict]:
        """
        Generate tweets for multiple movers

        Args:
            movers: DataFrame of movers
            contexts: Optional dict mapping team_player -> context string

        Returns:
            List of result dictionaries
        """
        results = []

        for _, mover in movers.iterrows():
            mover_dict = mover.to_dict()
            team_player = mover_dict['team_player']

            # Get context if provided
            context = None
            if contexts and team_player in contexts:
                context = contexts[team_player]

            result = self.generate_for_mover(mover_dict, context)
            results.append(result)

        return results

    def _fill_template(self, template: str, **kwargs) -> str:
        """
        Fill template with data

        Args:
            template: Template string
            **kwargs: Data to fill template

        Returns:
            Filled template string
        """
        # Get emojis
        emoji = TweetTemplates.get_emoji('fire', self.include_emojis)
        emoji2 = TweetTemplates.get_emoji('chart_up', self.include_emojis)
        team_emoji = TweetTemplates.get_emoji('football', self.include_emojis)

        # Handle player names (extract first name for possessive)
        team_player = kwargs.get('team_player', '')
        if ' ' in team_player and 'mvp' in kwargs.get('market', '').lower():
            # It's a player name for MVP
            player = team_player
        else:
            player = team_player

        # Prepare formatting data
        format_data = {
            'emoji': emoji,
            'emoji2': emoji2,
            'team_emoji': team_emoji,
            'team': kwargs.get('team_player', ''),
            'player': player,
            'team_player': team_player,
            'market': kwargs.get('market', ''),
            'last_odds': kwargs.get('last_odds', ''),
            'this_odds': kwargs.get('this_odds', ''),
            'change': kwargs.get('change', 0),
            'context': kwargs.get('context', 'Market moving on recent developments.')
        }

        try:
            return template.format(**format_data)
        except KeyError as e:
            # Fallback if template key missing
            return template

    def _format_american_odds(self, odds: float) -> str:
        """
        Format American odds with + or - sign

        Args:
            odds: Odds value

        Returns:
            Formatted odds string
        """
        odds_int = int(odds)
        if odds_int > 0:
            return f'+{odds_int}'
        else:
            return str(odds_int)

    def _generate_placeholder_context(self, mover: Dict) -> str:
        """
        Generate placeholder context when none provided

        Args:
            mover: Mover dictionary

        Returns:
            Placeholder context string
        """
        market = mover['market'].lower()
        direction = mover['direction']
        magnitude = mover['magnitude']

        if 'playoff' in market:
            if direction == 'up':
                return "Recent wins and strong performance have boosted their postseason outlook."
            else:
                return "Tough losses and mounting challenges have dimmed their playoff hopes."

        elif 'mvp' in market:
            if direction == 'up':
                return "Elite performance and key stats continuing to impress voters."
            else:
                return "Recent struggles and team performance affecting the narrative."

        elif any(x in market for x in ['super bowl', 'conference', 'champion']):
            if direction == 'up':
                return "Dominant play and favorable matchups strengthening championship case."
            else:
                return "Key losses and roster concerns raising questions about title hopes."

        else:
            if direction == 'up':
                return "Strong recent performance driving market confidence."
            else:
                return "Recent setbacks causing market to adjust expectations."

    def get_best_tweet(self, result: Dict) -> Dict:
        """
        Get the best tweet variation (shortest within limit)

        Args:
            result: Result dictionary with tweet drafts

        Returns:
            Best tweet draft
        """
        valid_tweets = [t for t in result['tweet_drafts'] if t['within_limit']]

        if not valid_tweets:
            # Return shortest one even if over limit
            return min(result['tweet_drafts'], key=lambda x: x['character_count'])

        # Return shortest valid tweet
        return min(valid_tweets, key=lambda x: x['character_count'])
