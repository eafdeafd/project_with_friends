import actions
import traceback

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    param_dict = {param['name'].lower() : param['value'] for param in parameters}

    if function == "query_aggregated_data":
        player_name = param_dict.get("player_name", "all")
        bracket = param_dict.get("bracket", ["vct-challengers", "vct-international", "game-changers"])
        region = param_dict.get("region", "all")
        past_games = param_dict.get("past_games", "all")
        agent = param_dict.get("agent", "all") 
        try:
            result_text = actions.query_aggregated_data(bracket, region, past_games, player_name, agent)
        except ValueError as e:
            print(f"Invalid input. Please provide valid input. Error = {e}. Stack trace: {traceback.format_exc()}")
            result_text = f"Invalid input. Please provide valid input. Error = {e}. Stack trace: {traceback.format_exc()}"
    elif function == "query_unaggregated_data":
        player_name = param_dict.get("player_name", "all")
        bracket = param_dict.get("bracket", ["vct-challengers", "vct-international", "game-changers"])
        region = param_dict.get("region", "all")
        past_games = param_dict.get("past_games", "all")
        agent = param_dict.get("agent", "all")
        try:
            result_text = actions.query_unaggregated_data(bracket, region, past_games, player_name, agent)
        except ValueError as e:
            print(f"Invalid input. Please provide valid input. Error = {e}. Stack trace: {traceback.format_exc()}")
            result_text = f"Invalid input. Please provide valid input. Error = {e}. Stack trace: {traceback.format_exc()}"

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/basdfedrock/latest/userguide/agents-lambda.html
    responseBody =  {
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
