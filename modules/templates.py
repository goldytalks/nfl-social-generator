"""
Tweet Templates Module
Contains templates for different market types and movement directions
"""
from typing import List, Dict


class TweetTemplates:
    """Template system for generating tweets based on market type"""

    # Emojis for different contexts
    EMOJIS = {
        'fire': '🔥',
        'chart_up': '📈',
        'chart_down': '📉',
        'eyes': '👀',
        'rocket': '🚀',
        'warning': '⚠️',
        'trophy': '🏆',
        'football': '🏈'
    }

    # Templates for "To Make The Playoffs" market
    PLAYOFFS_TEMPLATES = {
        'riser': [
            {
                'name': 'Version A - Bold',
                'template': '{emoji} BIGGEST MOVER: {team} playoff odds surged from {last_odds} to {this_odds} this week ({change:+.1f}%)\n\n{context}\n\nOur markets are reacting. Are you? {team_emoji}\n\n#NFL #SportsBetting'
            },
            {
                'name': 'Version B - Clean',
                'template': '{team} just became {this_odds} favorites to make the playoffs (was {last_odds} last week).\n\n{context}\n\nThe market knows. {emoji}\n\n#NFL'
            },
            {
                'name': 'Version C - Data-Driven',
                'template': 'Playoff probability alert: {team} odds moved {change:+.1f}% this week\n\n{last_odds} → {this_odds}\n\n{context}\n\n#NFL #BettingData'
            }
        ],
        'faller': [
            {
                'name': 'Version A - Bold',
                'template': '{emoji} FALLING FAST: {team} playoff odds dropped from {last_odds} to {this_odds} ({change:.1f}%)\n\n{context}\n\nOur markets don\'t miss. {emoji2}\n\n#NFL #SportsBetting'
            },
            {
                'name': 'Version B - Clean',
                'template': '{team} playoff odds took a hit this week: {last_odds} → {this_odds}\n\n{context}\n\nThe market has spoken. {emoji}\n\n#NFL'
            },
            {
                'name': 'Version C - Analytical',
                'template': 'Sharp movement detected: {team} playoff probability down {change:.1f}%\n\n{context}\n\nOur odds reflect the reality. {emoji}\n\n#NFL'
            }
        ]
    },

    # Templates for MVP market
    MVP_TEMPLATES = {
        'riser': [
            {
                'name': 'Version A - Hype',
                'template': '{emoji} MVP ODDS ALERT: {player}\'s odds surged to {this_odds} (was {last_odds})\n\n{context}\n\nThe race is heating up. {emoji2}\n\n#NFL #MVP'
            },
            {
                'name': 'Version B - Stats Focus',
                'template': '{player} MVP odds: {last_odds} → {this_odds} ({change:+.1f}%)\n\n{context}\n\nOur markets are watching. {emoji}\n\n#NFL'
            },
            {
                'name': 'Version C - Simple',
                'template': 'The {player} MVP case just got stronger.\n\nOdds moved from {last_odds} to {this_odds} this week.\n\n{context}\n\n#NFL #MVP'
            }
        ],
        'faller': [
            {
                'name': 'Version A - Direct',
                'template': '{emoji} {player} MVP odds cooling off: {last_odds} → {this_odds}\n\n{context}\n\nThe market adjusts. {emoji2}\n\n#NFL #MVP'
            },
            {
                'name': 'Version B - Analytical',
                'template': 'MVP odds shift: {player} down to {this_odds} (was {last_odds})\n\n{context}\n\nOur markets stay sharp. {emoji}\n\n#NFL'
            },
            {
                'name': 'Version C - Clean',
                'template': '{player}\'s MVP odds dropped {change:.1f}% this week.\n\n{context}\n\nThe race evolves. {emoji}\n\n#NFL #MVP'
            }
        ]
    },

    # Templates for Super Bowl / Conference Champion markets
    CHAMPIONSHIP_TEMPLATES = {
        'riser': [
            {
                'name': 'Version A - Bold',
                'template': '{emoji} CHAMPIONSHIP ODDS MOVING: {team} surged to {this_odds} (was {last_odds})\n\n{context}\n\nThe market believes. {team_emoji}\n\n#NFL #SuperBowl'
            },
            {
                'name': 'Version B - Clean',
                'template': '{team} {market} odds: {last_odds} → {this_odds}\n\n{context}\n\nOur markets don\'t sleep. {emoji}\n\n#NFL'
            },
            {
                'name': 'Version C - Hype',
                'template': 'The {team} are for real. {market} odds jumped {change:+.1f}% this week.\n\n{context}\n\nAre you paying attention? {emoji}\n\n#NFL'
            }
        ],
        'faller': [
            {
                'name': 'Version A - Direct',
                'template': '{emoji} {team} {market} odds falling: {last_odds} → {this_odds}\n\n{context}\n\nMarket sentiment shifting. {emoji2}\n\n#NFL'
            },
            {
                'name': 'Version B - Analytical',
                'template': 'Championship probability alert: {team} odds down {change:.1f}%\n\n{context}\n\nThe market reacts. {emoji}\n\n#NFL'
            },
            {
                'name': 'Version C - Clean',
                'template': '{team} {market} odds cooled to {this_odds} (was {last_odds})\n\n{context}\n\nOur odds stay current. {emoji}\n\n#NFL'
            }
        ]
    }

    # Generic fallback templates
    GENERIC_TEMPLATES = {
        'riser': [
            {
                'name': 'Version A - Generic',
                'template': '{emoji} BIG MOVER: {team_player} {market} odds up to {this_odds} (was {last_odds})\n\n{context}\n\nOur markets are live. {emoji2}\n\n#NFL #SportsBetting'
            },
            {
                'name': 'Version B - Simple',
                'template': '{team_player} odds movement: {last_odds} → {this_odds} ({change:+.1f}%)\n\n{context}\n\nThe market knows. {emoji}\n\n#NFL'
            }
        ],
        'faller': [
            {
                'name': 'Version A - Generic',
                'template': '{emoji} ODDS DROPPING: {team_player} {market} down to {this_odds} (was {last_odds})\n\n{context}\n\nOur markets stay sharp. {emoji2}\n\n#NFL #SportsBetting'
            },
            {
                'name': 'Version B - Simple',
                'template': '{team_player} odds fell {change:.1f}% this week.\n\n{context}\n\nMarket sentiment changing. {emoji}\n\n#NFL'
            }
        ]
    }

    @classmethod
    def get_templates(cls, market: str, direction: str) -> List[Dict]:
        """
        Get templates for specific market type and direction

        Args:
            market: Market type (e.g., "To Make The Playoffs")
            direction: "riser" or "faller"

        Returns:
            List of template dictionaries
        """
        # Normalize direction
        direction = direction.lower()
        if direction not in ['riser', 'faller']:
            direction = 'riser' if direction == 'up' else 'faller'

        # Map market to template set
        market_lower = market.lower()

        if 'playoff' in market_lower:
            templates = cls.PLAYOFFS_TEMPLATES.get(direction, [])
        elif 'mvp' in market_lower:
            templates = cls.MVP_TEMPLATES.get(direction, [])
        elif any(x in market_lower for x in ['super bowl', 'conference', 'champion']):
            templates = cls.CHAMPIONSHIP_TEMPLATES.get(direction, [])
        else:
            templates = cls.GENERIC_TEMPLATES.get(direction, [])

        return templates if templates else cls.GENERIC_TEMPLATES.get(direction, [])

    @classmethod
    def get_emoji(cls, emoji_key: str, include_emojis: bool = True) -> str:
        """
        Get emoji by key

        Args:
            emoji_key: Key for emoji
            include_emojis: Whether to include emojis

        Returns:
            Emoji string or empty string
        """
        if not include_emojis:
            return ''
        return cls.EMOJIS.get(emoji_key, '')

    @classmethod
    def get_team_emoji(cls, team_name: str) -> str:
        """
        Get team-specific emoji (placeholder for now)

        Args:
            team_name: Team name

        Returns:
            Team emoji or football emoji
        """
        # This could be expanded with team-specific emojis
        # For now, return football emoji
        return cls.EMOJIS['football']
