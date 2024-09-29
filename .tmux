###### VENV ####### 
# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]
then
    echo "Virtual environment is not activated Use \`${BYellow}pipenv ${BIWhite}shell${NC}\` command. Exiting..."
    exit 1
fi
###### Docker ####### 
# Check if Docker is running
if ! docker info &> /dev/null
then
   echo "Docker( ) is not running."
   sudo systemctl start docker   
fi

SESSIONNAME=$(basename "$(pwd)")

# check for session 
tmux has-session -t $SESSIONNAME &> /dev/null
if [ $? -ne 0 ];
 then
  # start the new session 
  tmux new-session -d -s $SESSIONNAME

  # Window 1: Open nvim on the current project root
  tmux new-window -t $SESSIONNAME:1 -n ''
  tmux send-keys -t $SESSIONNAME:1 'nvim' C-m

  # Window 2: Command line window
  tmux new-window -t $SESSIONNAME:2 -n ''

  # Window 3: Send docker compose up 
  tmux new-window -t $SESSIONNAME:3 -n '  '
  tmux send-keys -t $SESSIONNAME:3 'docker compose up -d' C-m

  # Window 4: Lazy docker 
  tmux new-window -t $SESSIONNAME:4 -n ' '
  tmux send-keys -t $SESSIONNAME:4 'lazydocker' C-m

fi

tmux attach -t $SESSIONNAME
