import actions

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    param_dict = {param['name'].lower() : param['value'] for param in parameters}

    if function == "build_team":
        bracket = param_dict.get("bracket")
        
        if bracket:
            try:
                result_text = actions.build_team(bracket)
            except ValueError as e:
                result_text = f"Invalid input. Please provide valid input. Error = {e}." 
    elif function == "query_data":
        bracket = param_dict.get("bracket", ["vct-challengers", "vct-international", "game-changers"])
        region = param_dict.get("region", "all")
        past_games = param_dict.get("past_games", "all")
        player_name = param_dict.get("player_name", "all")
        agent = param_dict.get("agent", "all")
        
        try:
            result_text = actions.query_data(bracket, region, past_games, player_name, agent)
        except ValueError as e:
            result_text = f"Invalid input. Please provide valid input. Error = {e}." 

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
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
