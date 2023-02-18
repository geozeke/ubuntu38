# Install this theme, by copying it to: ~/.oh-my-zsh/custom/themes
# Activate it by including this line in ~/.zshrc: ZSH_THEME="peter"

# No original work here! On 06/10/21, Peter Nardi cobbled together pieces from
# the fino and robbyrussell themes and tweaked them until it looked the way he
# wanted :-)

function virtualenv_prompt_info {
  [[ -n ${VIRTUAL_ENV} ]] || return
  echo "${ZSH_THEME_VIRTUALENV_PREFIX:=[}${VIRTUAL_ENV:t}${ZSH_THEME_VIRTUALENV_SUFFIX:=]}"
}

function prompt_char {
   echo "%(?:%{$fg_bold[green]%}➜ :%{$fg_bold[red]%}➜ )"
}

local ruby_env='$(ruby_prompt_info)'
local git_info='$(git_prompt_info)'
local virtualenv_info='$(virtualenv_prompt_info)'
local prompt_char='$(prompt_char)'

PROMPT="%{${virtualenv_info}%}%{${fg[green]}%}%n@%m ${fg[yellow]}in ${fg[blue]}%c%b ${git_info}${ruby_env}${fg_bold[green]}
${prompt_char}%{$reset_color%}"

ZSH_THEME_GIT_PROMPT_PREFIX="${fg[yellow]}on %{$reset_color%}${FG[255]}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="${FG[202]}✘✘✘"
ZSH_THEME_GIT_PROMPT_CLEAN="${FG[040]}✔"

ZSH_THEME_RUBY_PROMPT_PREFIX=" ${FG[239]}using${FG[243]} ‹"
ZSH_THEME_RUBY_PROMPT_SUFFIX="›%{$reset_color%}"

export VIRTUAL_ENV_DISABLE_PROMPT=1
ZSH_THEME_VIRTUALENV_PREFIX="${fg[yellow]}("
ZSH_THEME_VIRTUALENV_SUFFIX=") %{$reset_color%}"
