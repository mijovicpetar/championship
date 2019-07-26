"""Championship utils module."""

import traceback
from datetime import datetime
from sqlalchemy import text
from app.championship.models import League, LeagueGroup, FixtureResult, \
     FootballTeam, StandingsRow
from app import DB


class ChampionshipDataUtil:
    """Fixture data util class."""

    @classmethod
    def get_add_league(cls, league_name):
        """Get league, and add it if not exists.

        Args:
            league_name: League name.
        Returns:
            Added league object or None.

        """
        try:
            league = League.query.filter_by(title=league_name).first()

            if league is None:
                league = League(title=league_name)
                DB.session.add(league)
                DB.session.commit()
                DB.session.refresh(league)

            return league
        except:
            traceback.print_exc()
            return None

    @classmethod
    def get_league(cls, league_name):
        """Get league if exists.

        Args:
            league_name: League name.
        Returns:
            League object or None.

        """
        try:
            return League.query.filter_by(title=league_name).first()
        except:
            traceback.print_exc()
            return None

    @classmethod
    def get_add_group(cls, group_name, league_id):
        """Get group, and add it if not exists.
        Args:
            group_name: Group title.
            league_id: League id.
        Returns:
            Added group object or None
        """
        try:
            group = LeagueGroup.query.filter_by(
                title=group_name, league_id=league_id).first()

            if group is None:
                group = LeagueGroup(group_name, league_id)
                DB.session.add(group)
                DB.session.commit()
                DB.session.refresh(group)

            return group
        except:
            traceback.print_exc()
            return None

    @classmethod
    def get_group(cls, group_name, league_id):
        """Get group if exists.

        Args:
            group_name: Group title.
            league_id: League id.
        Returns:
            Group object or None

        """
        try:
            group = LeagueGroup.query.filter_by(
                title=group_name, league_id=league_id).first()

            return group
        except:
            traceback.print_exc()
            return None

    @classmethod
    def get_add_team(cls, team_name):
        """Get football team, and add it if not exists."""
        try:
            team = FootballTeam.query.filter_by(team_name=team_name).first()

            if team is None:
                team = FootballTeam(team_name)
                DB.session.add(team)
                DB.session.commit()
                DB.session.refresh(team)

            return team
        except:
            traceback.print_exc()
            return None

    @classmethod
    def add_fixture_result(cls, data_dict):
        """Add one fixture result.

        Args:
            data_dict: Data JSON.
        Returns:
            Boolean: True if added or False otherwise.

        """
        try:
            home_team_id = cls.get_add_team(data_dict.get('homeTeam')).id
            away_team_id = cls.get_add_team(data_dict.get('awayTeam')).id
            league_id = cls.get_add_league(data_dict.get('leagueTitle')).id
            group_id = cls.get_add_group(
                data_dict.get('group'), league_id).id

            matchday = data_dict['matchday']
            kickoff_at = data_dict['kickoffAt']
            score = data_dict['score']

            fixture_result = FixtureResult(group_id, home_team_id,
                                           away_team_id, matchday, kickoff_at,
                                           score)

            DB.session.add(fixture_result)
            DB.session.commit()
            DB.session.refresh(fixture_result)

            return fixture_result
        except:
            traceback.print_exc()
            return None

    @classmethod
    def update_fixture_result(cls, result_id, data_dict):
        """Edit fixture result.

        Args:
            data_dict: Data JSON.
        Returns:
            tuple: True if edited or False otherwise, reason.

        """
        try:
            fixture = FixtureResult.query.get(result_id)

            if fixture is None:
                return False, 'Fixture not found.'

            fixture.score = data_dict['score']

            DB.session.commit()

            return True, 'Success'
        except:
            traceback.print_exc()
            return False, 'Exception occured.'

    @classmethod
    def update_fixture_results(cls, results):
        """Update fixture results.

        Args:
            results: Array of results to update.
        Returns:
            Status message.

        """
        if not isinstance(results, list):
            results = [results]

        for result in results:
            cls.update_fixture_result(result.get('id'), result)

    @classmethod
    def __create_standings_dict(cls, fixtures):
        """Extract team ids from fixtures and create standings dictionary.

        Args:
            fixtures: Match results.
        Returns:
            Dictionary of unique team ids : stats dict.

        """
        result = []
        for fixture in fixtures:
            result.append(fixture.home_team_id)
            result.append(fixture.away_team_id)

        # Create set of unique team ids.
        unique_result = set(result)

        # Create standings dict
        standings_dict = {}
        for item in unique_result:
            team_name = FootballTeam.query.get(item).team_name
            standings_item = StandingsRow(team=team_name)
            standings_dict[item] = standings_item

        return standings_dict

    @classmethod
    def __parse_result(cls, standings_dict, fixture_result):
        """Parse result and update stats.

        Args:
            standings_dict: Standings dictionary.
            fixture_result: Fixture result.

        """
        # Here we get stats dict for team.
        home_team = standings_dict[fixture_result.home_team_id]
        away_team = standings_dict[fixture_result.away_team_id]

        splited_score = fixture_result.score.split(':')
        home_score = int(splited_score[0])
        away_score = int(splited_score[1])

        # Points calculation.
        if home_score > away_score:
            home_team.points += 3
            home_team.win += 1
            away_team.lose += 1
        elif away_score < home_score:
            away_team.points += 3
            away_team.win += 1
            home_team.lose += 1
        else:
            home_team.points += 1
            home_team.draw += 1
            away_team.points += 1
            away_team.draw += 1

        # Other home team stats updates.
        home_team.played_games += 1
        home_team.goals += home_score
        home_team.goals_against += away_score
        home_team.goal_difference += home_score - away_score

        # Other away team stats updates.
        away_team.played_games += 1
        away_team.goals += away_score
        away_team.goals_against += home_score
        away_team.goal_difference += away_score - home_score

    @classmethod
    def __get_sorted_stangings_as_list(cls, standings_dict):
        """Sort the standings and return as list.
        Args:
            stangings_dict: Standigs dictionary.
        Returns:
            List: Sorted standings as list.
        """
        standings = list(standings_dict.values())
        standings.sort(reverse=True)

        index = 1
        for standing in standings:
            standing.rank = index
            index += 1

        return standings

    @classmethod
    def __gen_standing_table(cls, group_id):
        """Generator method for standings table.

        Args:
            group_id: Group id.
        Returns:
            Standings table dict.

        """
        # Get fixtures for group and create standings dict.
        fixtures = FixtureResult.query.filter_by(group_id=group_id).all()
        standings_dict = cls.__create_standings_dict(fixtures)

        # Populate standings data.
        max_matchday = 0
        for fixture_result in fixtures:
            if fixture_result.matchday > max_matchday:
                max_matchday = fixture_result.matchday
            cls.__parse_result(standings_dict, fixture_result)

        # Sort the standings and get as a list.
        standings = cls.__get_sorted_stangings_as_list(standings_dict)

        # Complete output
        group = LeagueGroup.query.get(group_id)
        group_title = group.title
        league_title = League.query.get(group.league_id).title
        group_table = {
            'leagueTitle': league_title,
            'matchday': max_matchday,
            'group': group_title,
            'standing': []
        }

        for standing in standings:
            group_table['standing'].append(standing.to_result_dict())

        return group_table

    @classmethod
    def handle_fixture_results(cls, data):
        """Handle passed fixture results.

        Args:
            data: List of match results to add.
        Returns:
            Standings for all groups added.

        """
        # Handle one result which is not sent in list.
        if not isinstance(data, list):
            data = [data]

        unique_group_ids = set()
        # Add the results and create unique set of groups to genereate tables.
        for fixture in data:
            league_id = cls.get_add_league(fixture.get('leagueTitle')).id
            group_id = cls.get_add_group(
                fixture.get('group'), league_id).id
            unique_group_ids.add(group_id)
            cls.add_fixture_result(fixture)

        standings = []
        for group_id in unique_group_ids:
            standing = cls.__gen_standing_table(group_id)
            standings.append(standing)

        # If data for one group only.
        if len(standing) == 1:
            standings = standings[0]

        return standings

    @classmethod
    def get_tabels_for_groups(cls, target_groups=None):
        """Get all tabels for all groups.

        Args:
            target_groups: Dict - leagueName, group.
        Returns:
            List of standing tabels.

        """
        groups = []
        if target_groups is not None:
            # Specified groups.
            for target_group in target_groups:
                league_name = target_group['leagueName']
                group_name = target_group['group']
                league = cls.get_league(league_name)
                if league is None:
                    continue

                group = cls.get_group(group_name, league.id)
                if group is None:
                    continue

                groups.append(group)
        else:
            # All groups.
            groups = LeagueGroup.query.all()

        tabels = []
        for group in groups:
            temp_table = cls.__gen_standing_table(group.id)
            tabels.append(temp_table)

        # In case of one group don't return list.
        if len(tabels) == 1:
            result = tabels[0]
        else:
            result = tabels

        return result

    @classmethod
    def __parse_query_row(cls, row):
        """Parse query row.

        Args:
            row: Result row of custom query.
        Returns:
            Dictionary.

        """
        res_id = row['id']
        group_id = row['group_id']
        matchday = row['matchday']
        kickoff_at = row['kickoff_at']
        score = row['score']
        home_team_id = row['home_team_id']
        away_team_id = row['away_team_id']

        temp_fixture = FixtureResult(group_id,
                                     home_team_id,
                                     away_team_id,
                                     matchday,
                                     kickoff_at,
                                     score,
                                     res_id)

        return temp_fixture.to_result_dict()


    @classmethod
    def filter_results(cls, filters_dict):
        """Generator for filtering existing results based on filters dict.

        Args:
            filters_dict: Dictionary of filters to use.
        Result:
            Array of results that match the filters.

        """
        if filters_dict is None:
            filters_dict = {}

        try:
            group_filter = filters_dict.get('group')
            team_filter = filters_dict.get('team')
            date_from_filter = filters_dict.get('date_from')
            date_to_filter = filters_dict.get('date_to')

            filters = [
                group_filter, team_filter, date_from_filter, date_to_filter
            ]

            query = 'select * from fixture_results'

            if any(filters):
                query = 'select '
                query += 'fixture_results.id, matchday, kickoff_at, score, '
                query += 'group_id, home_team_id, away_team_id '
                query += 'from fixture_results, football_teams, league_groups'
                query += ' where '

            if team_filter:
                query += '(fixture_results.home_team_id = football_teams.id'
                query += ' or '
                query += 'fixture_results.away_team_id = football_teams.id)'
                query += ' and '
                query += "football_teams.team_name = '{}'".format(team_filter)
            if group_filter:
                query += ' and league_groups.id = fixture_results.group_id '
                query += "and league_groups.title='{}'".format(group_filter)
            if date_from_filter:
                date_from = datetime.strptime(
                    date_from_filter, '%Y-%m-%dT%H:%M:%S')
                date_from = str(date_from)
                query += ' and '
                query += "fixture_results.kickoff_at >= '{}'".format(date_from)
            if date_to_filter:
                date_to = datetime.strptime(
                    date_to_filter, '%Y-%m-%dT%H:%M:%S')
                date_to = str(date_to)
                query += ' and '
                query += "fixture_results.kickoff_at <= '{}'".format(date_to)

            print(query)
            sql_query = text(query)
            rows = DB.engine.execute(sql_query)

            res = []
            for row in rows:
                temp_res = cls.__parse_query_row(row)
                res.append(temp_res)

            return res
        except:
            traceback.print_exc()
            return []
