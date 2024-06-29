
from utils import execute_shell, check_service_monitors_crd, check_command, replace_line_in_file_with_sed, get_line_with_grep


def main():
    # check all the required programs needed
    pre_req_validation = check_command('kubectl')
    pre_req_validation = check_command('helm')
    pre_req_validation = check_command('docker')
    pre_req_validation = check_command('terraform')

    if pre_req_validation:
        print("//////////////////////////////////////")
        print("Welcome to the Gaia Deployment Script!")
        print("//////////////////////////////////////")
        print('\n')
        print("Please choose one of the following options:")
        print('\n')
        print("1) Run gaia from remote")
        print("2) Run gaia from local docker file")
        print("3) Apply k8s manifests to current context cluster")
        print("4) Replace Docker Configurable Values")
        print('\n')
        choice = input("Enter your choice (1, 2, 3, or 4): ")

        if choice in ['1', '2', '3', '4']:
            if choice == '1':
                print("You chose to run Gaia from remote.")
                # run from remote
                execute_shell(["docker", "run", "ajail/gaia:v17.2.0"])
            elif choice == '2':
                print("You chose to run Gaia from local docker file.")
                # build from local docker file
                execute_shell(["docker", "build", "../docker", "-t", "gaia"])
                execute_shell(["docker", "run", "gaia"])
            elif choice == '3':
                print("You chose to apply k8s manifests to current context cluster.")
                # check if ServiceMonitor CDR is installed, if not, install ServiceMonitor CDR via helm
                if not check_service_monitors_crd():
                    execute_shell(["helm", "repo", "add", "prometheus-community",
                                  "https://prometheus-community.github.io/helm-charts"])
                    execute_shell(["helm", "repo", "update"])
                    execute_shell(["helm", "install", "prometheus-operator",
                                  "prometheus-community/kube-prometheus-stack"])
                # apply manifest to kubectl current context
                execute_shell(["kubectl", "apply", "-f",
                              "../k8s/gaia-statefulset.yml"])
                execute_shell(["kubectl", "apply", "-f",
                              "../k8s/gaia-service.yml"])
                execute_shell(["kubectl", "apply", "-f",
                              "../k8s/gaia-servicemonitor.yml"])
                print('\nDone! User "kubectl get pods" command to observe the pods initializing and running.  Give them time to come online!')
            elif choice == '4':
                # grep the env vars from docker file
                # store them in variables
                # append the variables onto a list
                print("You chose to replace configurable values.")
                docker_file_path = '../docker/Dockerfile'
                current_chain_name = get_line_with_grep(
                    docker_file_path, 'ENV CHAIN_NAME=')
                current_initial_validator = get_line_with_grep(
                    docker_file_path, 'ENV INITIAL_VALIDATOR=')
                current_keyring_backend = get_line_with_grep(
                    docker_file_path, 'ENV KEYRING_BACKEND=')
                current_minimum_gas_price = get_line_with_grep(
                    docker_file_path, 'ENV MINIMUM_GAS_PRICE=')
                current_initial_validator_balance = get_line_with_grep(
                    docker_file_path, 'ENV INITIAL_VALIDATOR_BALANCE=')
                current_initial_validator_stake = get_line_with_grep(
                    docker_file_path, 'ENV INITIAL_VALIDATOR_STAKE=')

                current_envs = list()
                current_envs.append(current_chain_name)
                current_envs.append(current_initial_validator)
                current_envs.append(current_keyring_backend)
                current_envs.append(current_minimum_gas_price)
                current_envs.append(current_initial_validator_balance)
                current_envs.append(current_initial_validator_stake)

                # loop through the env vars and replace with new input (if available).
                count = 0
                while True:
                    env_name = current_envs[count].split('=')[0]
                    env_value = current_envs[count].split('=')[1]
                    print('\n')
                    print(f"Replace value for {current_envs[count]}?")
                    new_val = input(
                        f"Enter new value (default: {env_value}): ").strip()
                    if new_val:
                        new_env_val = f'{env_name}="{new_val}"'
                        replace_line_in_file_with_sed(
                            docker_file_path, current_envs[count], new_env_val)
                    count += 1
                    if count == len(current_envs):
                        break
        else:
            print("Invalid choice. Exiting.")
            exit()
    else:
        print("Pre-requisite validation failed.  Please ensure you have the following installed:")
        print('\n')
        print('kubectl\n')
        print('helm\n')
        print('docker\n')
        print('terraform\n')


if __name__ == "__main__":
    main()
