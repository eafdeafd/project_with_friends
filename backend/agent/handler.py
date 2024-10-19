import actions

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    param_dict = {param['name'].lower() : int(param['value']) for param in parameters}

    if function == "get_top_players_by_role":
        team_setting = param_dict.get("team_setting")
        role = param_dict.get("role")
        player_data = param_dict.get("player_data")
        
        if team_setting and role:
            try:
                result_text = actions.get_top_players_by_role(team_setting, role, player_data)
            except ValueError:
                result_text = "Invalid input. Please provide valid input." 

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

    dummy_function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(dummy_function_response))

    return dummy_function_response
