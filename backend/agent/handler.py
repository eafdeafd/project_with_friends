import actions
import traceback

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    param_dict = {param['name'].lower() : param['value'] for param in parameters}

    try:
        if function == "query_past_games":
            player_name = param_dict.get("player_name")
            if not player_name:
                raise ValueError("player_name parameter is required for query_past_games function.")
            past_games = int(param_dict.get("past_games", 5))
            agent = param_dict.get("agent", "all")
            result_text = actions.query_past_games(player_name, past_games, agent)
        elif function == "get_players_from_specifiers":
            role = param_dict.get("role")
            if not role:
                raise ValueError("role parameter is required for get_players_from_specifiers function.")
            bracket = param_dict.get("bracket")
            if not bracket:
                raise ValueError("bracket parameter is required for get_players_from_specifiers function.")
            region = param_dict.get("region", "all")
            agent = param_dict.get("agent", "all")
            IGL = param_dict.get("igl", False)
            result_text = actions.get_players_from_specifiers(role, bracket, region, agent, IGL)
        elif function == "query_player":
            player_name = param_dict.get("player_name")
            if not player_name:
                raise ValueError("player_name parameter is required for query_player function.")
            result_text = actions.query_player(player_name)
        else:
            raise ValueError(f"Function {function} is not recognized.")
    except ValueError as e:
        print(f"Invalid input. Please provide valid input. Error = {e}. Stack trace: {traceback.format_exc()}")
        result_text = f"Invalid input. Please provide valid input. Error = {e}. Stack trace: {traceback.format_exc()}"
    
    responseBody = {
        "TEXT": {
            "body": result_text
        }
    }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}

    return function_response
