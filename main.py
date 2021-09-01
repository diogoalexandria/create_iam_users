import sys
import boto3
from args import args_parser
from account import get_account
from keeper_secrets_manager_core import SecretsManager
def main(command, params):
    if command == "--help" or command == "-h":
        print(" - You can use the command 'create-app-user'")
    elif command == "create-app-user":
        params_dict = {
            "team": None,
            "app": None,
            "policy": None
        }
        if params:
            for param in params:
                param = param.split("=")

                key = param[0]
                value = param[1]

                valid_keys = params_dict.keys()

                if key in valid_keys:
                    params_dict[key] = value
                
            if params_dict["team"] and params_dict["app"]:
                team = params_dict["team"]
                app = params_dict["app"]

                user_name = f'{team}.{app}'

                client = boto3.client("iam")
                try: 
                    user_response = client.create_user(                                
                        UserName=user_name,                            
                        Tags=[
                            {
                                "Key": "team",
                                "Value": team
                            },
                        ]
                    )
                    if user_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        print(" - Create user: ok")
                    
                    user_to_group_response = client.add_user_to_group(
                        GroupName="applications",
                        UserName=user_name
                    )
                    if user_to_group_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        print(" - Add user to group: ok")

                    access_key_response = client.create_access_key(
                        UserName=user_name
                    )
                    if access_key_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        print(" - Create access key: ok")

                    access_key_id = access_key_response["AccessKey"]["AccessKeyId"]
                    secret_access_key = access_key_response["AccessKey"]["SecretAccessKey"]                    
                
                    if params_dict["policy"]:
                        try:
                            policy_arn = f'arn:aws:iam::{get_account()}:policy/{params_dict["policy"]}'
                            response = client.attach_user_policy(
                                UserName=user_name,
                                PolicyArn=policy_arn
                            )
                            print(" - Policy attach: ok")
                        except Exception as excpetion:
                            print("Something went wrong trying attach policy")
                            print(f'Arn tried: {policy_arn}')
                            print(f'Exception: {excpetion}')
                            pass
                    else:
                        print(" - No policy was passed\n")

                    print(f'\n - Access key id: {access_key_id}')
                    print(f' - Secret Access key: {secret_access_key}')

                except client.exceptions.EntityAlreadyExistsException:
                    print(f' - User {user_name} already exists')

                
            else:
                print(
                    " - Command missing params\n",
                    "- Params:\n",
                    "   team=<team-name> [Required]\n",
                    "   app=<app-name> [Required]\n",
                    "   policy=<policy-name>"
                )

        else:            
            print(
                " - Command without params\n",
                "- Params:\n",
                "   team=<team-name> [Required]\n",
                "   app=<app-name> [Required]\n",
                "   policy=<policy-name>"
            )            
            
    else:
        print(" - Command not recognized")
        print(" - Try '--help' or '-h' to know more")

if __name__ == "__main__":
    command, params =  args_parser(sys.argv)    
             
    main(command, params)
