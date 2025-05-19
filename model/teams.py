from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Team:
    ID: int #chiave
    year:int
    teamCode:str
    divID:str
    div_ID:int
    teamRank:int
    games:int
    gamesHome:int
    wins:int
    losses:int
    divisionWinnner:str
    leagueWinner:str
    worldSeriesWinnner:str
    runs:int
    hits:int
    homeruns:int
    stolenBases:int
    hitsAllowed:int
    homerunsAllowed:int
    name:str
    park:str


    def __hash__(self):
        return self.ID

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.ID == other.ID