"""Auth models."""

from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from app import DB


class League(DB.Model):
    """League model."""
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)

    def __init__(self, title):
        """Init method.

        Args:
            title: League title.

        """
        self.title = title


class LeagueGroup(DB.Model):
    """League group model."""
    __tablename__ = 'league_groups'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    league_id = Column(Integer, ForeignKey(League.id))

    def __init__(self, title, league_id):
        """Init method.

        Args:
            title: Group title.
            league_id: Id of parent league.

        """
        self.title = title
        self.league_id = league_id


class FootballTeam(DB.Model):
    """Football team model."""
    __tablename__ = 'football_teams'

    id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True)

    def __init__(self, team_name):
        """Init method."""
        self.team_name = team_name


class FixtureResult(DB.Model):
    """Match model."""
    __tablename__ = 'fixture_results'

    id = Column(Integer, primary_key=True)
    matchday = Column(Integer)
    kickoff_at = Column(DateTime)
    score = Column(String)
    group_id = Column(Integer, ForeignKey(LeagueGroup.id))
    home_team_id = Column(Integer, ForeignKey(FootballTeam.id))
    away_team_id = Column(Integer, ForeignKey(FootballTeam.id))

    def __init__(self, group_id, home_team_id, away_team_id, matchday=None,
                 kickoff_at=None, score=None, res_id=None):
        """Init method.
        Args:
            group_id: If of parent group.
            home_team_id: Id of home team.
            away_team_id: Id of away team.
            matchday: Matchday presented in number.
            kickoff_at: DateTime as string presenting kick of.
            score: Score in string format 3:2.
        """
        if res_id is not None:
            self.id = res_id
        self.group_id = group_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.matchday = matchday
        # Some dates have month in the middle, some month
        # at the end, in the data set.
        if isinstance(kickoff_at, datetime):
            self.kickoff_at = kickoff_at
        else:
            self.kickoff_at = datetime.strptime(kickoff_at, '%Y-%m-%dT%H:%M:%S')
        self.score = score

    def to_result_dict(self):
        """To result dict."""
        group = LeagueGroup.query.get(self.group_id)
        group_title = group.title
        league_title = League.query.get(group.league_id).title
        home_team = FootballTeam.query.get(self.home_team_id)
        away_team = FootballTeam.query.get(self.away_team_id)

        result_dict = {
            'id': self.id,
            'matchday': self.matchday,
            'kickoffAt': self.kickoff_at.strftime('%Y-%m-%dT%H:%M:%S'),
            'score': self.score,
            'group': group_title,
            'leagueTitle': league_title,
            'homeTeam': home_team.team_name,
            'awayTeam': away_team.team_name
        }

        return result_dict


class StandingsRow:
    """Model for standings row."""

    def __init__(self, rank=-1, team='', played_games=0, points=0, goals=0,
                 goals_against=0, goal_difference=0, win=0, lose=0, draw=0,
                 matchday=0):
        """Init method."""
        self.rank = rank
        self.team = team
        self.played_games = played_games
        self.points = points
        self.goals = goals
        self.goals_against = goals_against
        self.goal_difference = goal_difference
        self.win = win
        self.lose = lose
        self.draw = draw
        self.matchday = matchday

    def __eq__(self, other):
        """Equal overload."""
        points_equal = self.points == other.points
        gd_equal = self.goal_difference == other.goal_difference

        return points_equal and gd_equal

    def __lt__(self, other):
        """Lower than overload."""
        result = None
        if self.points < other.points:
            result = True
        elif self.points > other.points:
            result = False
        else:
            result = self.goal_difference < other.goal_difference

        return result

    def __gt__(self, other):
        """Greater than overload."""
        if self.points > other.points:
            result = True
        elif self.points < other.points:
            result = False
        else:
            result = self.goal_difference > other.goal_difference

        return result

    def to_result_dict(self):
        """Converts to dict in format provided."""
        result_dict = {
            'rank': self.rank,
            'team': self.team,
            'playedGames': self.played_games,
            'points': self.points,
            'goals': self.goals,
            'goalsAgainst': self.goals_against,
            'goalDifference': self.goal_difference,
            'win': self.win,
            'lose': self.lose,
            'draw': self.draw
        }

        return result_dict
