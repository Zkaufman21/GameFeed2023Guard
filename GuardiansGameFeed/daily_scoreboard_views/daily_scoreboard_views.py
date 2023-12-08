import pandas as pd
from django.http import HttpRequest, JsonResponse
import statsapi


def getBoxScoreData(row: pd.Series):
    return statsapi.boxscore_data(row['game_id'])


def getLineScoreData(row: pd.Series):
    return statsapi.linescore(row['game_id'])


def retrieve_daily_scoreboard_data_view(request: HttpRequest) -> JsonResponse:
    date = request.GET['date']
    games = pd.DataFrame(
        statsapi.schedule(sportId=1, start_date=date, end_date=date)
    )
    box_scores = pd.DataFrame(games.apply(getBoxScoreData, axis=1).tolist())
    line_scores = pd.DataFrame(games.apply(getLineScoreData, axis=1).tolist())

    response_data = {'games': games.to_dict(orient="records"), 'box_scores': box_scores.to_dict(orient="records"), 'line_scores': line_scores.to_dict(orient="records")}
    return JsonResponse(response_data)

