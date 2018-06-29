import csv
from pydfs_lineup_optimizer.exceptions import LineupOptimizerIncorrectCSV
from pydfs_lineup_optimizer.lineup_importer import CSVImporter
from pydfs_lineup_optimizer.player import Player


class FanDuelCSVImporter(CSVImporter):
    def import_players(self):  # pragma: no cover
        players = []
        with open(self.filename, 'r') as csvfile:
            csv_data = csv.DictReader(csvfile, skipinitialspace=True)
            for row in csv_data:
                try:
                    max_exposure = row.get('Max Exposure')
                    player = Player(
                        row['Id'],
                        row['First Name'],
                        row['Last Name'],
                        row['Position'].split('/'),
                        row['Team'],
                        float(row['Salary']),
                        float(row['FPPG']),
                        True if row['Injury Indicator'].strip() else False,
                        max_exposure=float(max_exposure.replace('%', '')) if max_exposure else None
                    )
                except KeyError:
                    raise LineupOptimizerIncorrectCSV
                players.append(player)
        return players
