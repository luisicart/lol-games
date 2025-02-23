from dotenv import load_dotenv
import os
import pandas as pd
import httpx
from functools import partial
from aiometer import run_all
import asyncio 

load_dotenv()
api_key = os.environ.get('riot_api_key')
limit_requests_per_second = 0.8  # Metade do limite da API

database_path = f"{os.getcwd()}/data"

def get_soloq_leaderboard(top=None):
    root = "https://br1.api.riotgames.com/"
    endpoints = {
        "challenger_endpoint": "lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5",
        "grandmaster_endpoint": "lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5",
        "master_endpoint": "lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5"
    }
    responses = {}
    dataframes = {}

    for name, endpoint in endpoints.items():
        response = httpx.get(f"{root}{endpoint}?api_key={api_key}")
        responses[f"{name}_response"] = response

    for name, response in responses.items():
        rank_name = name.split('_')[0]
        df = pd.DataFrame(response.json()['entries'])
        dataframes[f'{rank_name}_df'] = df

    leaderboard_df = (
        pd.concat(dataframes.values(), ignore_index=True)
        .drop(columns='rank')
        .sort_values('leaguePoints', ascending=False)
        .reset_index(drop=True)
        .rename_axis('rank').reset_index()
        .sort_values('rank', ascending=True)
        .query('leaguePoints > 0')
        .rename(columns={
            'summonerId': 'summoner_id',
            'leaguePoints': 'league_points',
            'freshBlood': 'fresh_blood',
            'hotStreak': 'hot_streak',
        })
    )
    leaderboard_df['rank'] += 1
    return leaderboard_df

async def get_matches(puuid, nr_matches):
    async with httpx.AsyncClient(base_url='https://americas.api.riotgames.com') as client:
    
        response = await client.get(f"lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start=0&count={nr_matches}&api_key={api_key}")
        print('Get matches: ', response.status_code)
        matches = response.json()

        return {
            "puuid": puuid,
            "nr_matches": len(matches),
            "matches": matches
        }

async def get_match_info(match_id):
    async with httpx.AsyncClient(base_url='https://americas.api.riotgames.com') as client:
        response = await client.get(f'lol/match/v5/matches/{match_id}?api_key={api_key}')
        print("Get match info, status:", response.status_code)
        match_info = response.json()
        return {"match_id": match_id, **match_info}

async def fetch_puuids_and_matches():

    df_leaderboard = get_soloq_leaderboard()

    df_leaderboard.to_parquet(f"{database_path}/df_leaderboard.parquet", engine="pyarrow", index=False)
    print("Leaderboard salvo no banco de dados.")

    summoners = df_leaderboard['puuid'].to_list()[:3]

    puuid_result = await run_all(
        [partial(get_matches, puuid, 3) for puuid in summoners],
        max_per_second=limit_requests_per_second,
        max_at_once=3
    )
    df_matches_per_puuid = pd.DataFrame(puuid_result)

    df_matches_per_puuid.drop(columns=["matches"]).to_parquet(f"{database_path}/df_matches_per_puuid.parquet", engine="pyarrow", index=False)
    print("Matches por PUUID salvos no banco de dados.")

    all_match_ids = [match for matches in df_matches_per_puuid["matches"] for match in matches]
    match_details = await run_all(
        [partial(get_match_info, match_id) for match_id in all_match_ids],
        max_per_second=limit_requests_per_second,
        max_at_once=3
    )
    df_match_info = pd.DataFrame(match_details).drop_duplicates(subset=['match_id'])

    df_match_info.to_parquet(f"{database_path}/df_match_info.parquet", engine="pyarrow", index=False)

    return df_leaderboard, df_matches_per_puuid, df_match_info

if __name__ == "__main__":

    df_leaderboard, df_matches_per_puuid, df_match_info = asyncio.run(fetch_puuids_and_matches())
    
    print("\nLeaderboard:")
    print(df_leaderboard)
    
    print("\nMatches por PUUID:")
    print(df_matches_per_puuid)
    
    print("\nInformações das partidas:")
    print(df_match_info)