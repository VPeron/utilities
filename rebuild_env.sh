#!/bin/zsh

# deactivate if an env is activated
pyenv deactivate
# delete current env
pyenv virtualenv-delete sec_portfolio_env

# rebuild env
pyenv virtualenv sec_portfolio_env

# activate env
pyenv activate sec_portfolio_env

# update pip
pip install --upgrade pip

# rebuild requirements
pip install -r requirements.txt