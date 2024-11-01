#!/bin/bash

python main.py config.toml
python main.py config.toml --database.port="1111" --database.username=new_user
python main.py config.toml --database.port="1111" --database.username=new_user --global.log_level=info
python main.py config.toml --database.port="1111" --database.username=new_user --global.log_level=error
python main.py config.toml --aaa.param1=valeur1
python main.py config.toml --aaa.param1=[1,2,3]
