# handler.py
import actions
import traceback
import json

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    # Convert parameters list to a dictionary
    param_dict = {param['name'].lower(): param['value'] for param in parameters}

    try:
        if function == "query_past_games":
            player_name = param_dict.get("player_name")
            if not player_name:
                raise ValueError("player_name parameter is required for query_past_games function.")
            past_games = int(param_dict.get("past_games", 5))
            agent = param_dict.get("agent", "all")
            result_text = actions.query_past_games(player_name, past_games, agent)
        elif function == "get_players_from_specifiers":
            # Get parameters from param_dict, expecting arrays
            role = param_dict.get("role")
            if not role:
                raise ValueError("role parameter is required for get_players_from_specifiers function.")
            bracket = param_dict.get("bracket")
            if not bracket:
                raise ValueError("bracket parameter is required for get_players_from_specifiers function.")
            igl = param_dict.get("igl")
            if igl is None:
                raise ValueError("igl parameter is required for get_players_from_specifiers function.")
            region = param_dict.get("region", ["all", "all", "all", "all", "all"])
            agent = param_dict.get("agent", ["all", "all", "all", "all", "all"])

            # Ensure all parameters are lists
            def ensure_list(param, default_length=5, default_value='all'):
                if isinstance(param, list):
                    return param
                else:
                    return [param] * default_length

            role = ensure_list(role)
            bracket = ensure_list(bracket)
            igl = ensure_list(igl)
            region = ensure_list(region)
            agent = ensure_list(agent)

            # Validate lengths and fill or truncate lists to length 5
            def adjust_list(lst, default_value, desired_length=5):
                if len(lst) < desired_length:
                    lst.extend([default_value] * (desired_length - len(lst)))
                return lst[:desired_length]

            role = adjust_list(role, 'all')
            bracket = adjust_list(bracket, 'all')
            igl = adjust_list(igl, False)
            region = adjust_list(region, 'all')
            agent = adjust_list(agent, 'all')

            # Convert igl to boolean list
            igl = [str(item).lower() == 'true' for item in igl]

            # Call the function with the adjusted parameters
            result_text = actions.get_players_from_specifiers(role, bracket, igl, region, agent)
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
