__author__ = 'yetone'

from script_manager import Manager
from collipa.app import app_manager

manager = Manager(description="The collipa script manager")

manager.add_command('app', app_manager)


if __name__ == '__main__':
    manager.run()
