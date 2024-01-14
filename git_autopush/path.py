import os
import getpass

# Get the current user
current_user = getpass.getuser()

# Construct the path using the current user
path_to_add = f'/home/{current_user}/.local/bin'

# Retrieve the current path
current_path = os.environ.get('PATH', '')

if path_to_add not in current_path:
    new_path = f'{current_path}:{path_to_add}'
    os.environ['PATH'] = new_path

    # Add the path to .bashrc
    with open(f'/home/{current_user}/.bashrc', 'a') as bashrc_file:
        bashrc_file.write(f'export PATH=$PATH:{path_to_add}\n')

    # Add the path to .zshrc
    with open(f'/home/{current_user}/.zshrc', 'a') as zshrc_file:
        zshrc_file.write(f'export PATH=$PATH:{path_to_add}\n')
