export AACTIVATOR_VERSION=1.0.1
alias aactivator=/home/jbpratt/.local/bin/aactivator
unset AACTIVATOR_ACTIVE
if [ "$ZSH_VERSION" ]; then
    precmd_aactivator() { if [ -x /home/jbpratt/.local/bin/aactivator ]; then  eval "`/home/jbpratt/.local/bin/aactivator`"; fi; }
    if ! [ "${precmd_functions[(r)precmd_aactivator]}" ]; then
        precmd_functions=(precmd_aactivator $precmd_functions)
    fi
else
    if ! ( echo "$PROMPT_COMMAND" | grep -Fq 'if [ -x /home/jbpratt/.local/bin/aactivator ]; then  eval "`/home/jbpratt/.local/bin/aactivator`"; fi' ); then
        PROMPT_COMMAND='if [ -x /home/jbpratt/.local/bin/aactivator ]; then  eval "`/home/jbpratt/.local/bin/aactivator`"; fi; '"$PROMPT_COMMAND"
    fi
fi
