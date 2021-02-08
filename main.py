from datetime import datetime
import configparser
import argparse

class TimeLog:

    def __init__(self):
        timedate = datetime.now()
        self.time = timedate.strftime("%H-%M-%S")
        self.date = timedate.strftime("%m-%d-%Y")
        self.config_file = f'{self.date}.ini'

    def create_task(self, task):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        task_number = 1
        if config.sections():
            task_number = max([int(section) for section in config.sections()]) + 1

        config[task_number] = {
            'name': task['name'],
            'description': task['desc'],
            'est_time': task['est_time'],
            'usefulness': 'NA',
            'completed': 'N',
            'completed_notes': '',
            f'log_{self.time}': 'task created'
            }
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)



        print('Created task', task['name'])
        print(config.sections())

    def add_log(self, task=None):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        if not task['id']:
            print('Please choose task from:')
            for idx, section in enumerate(config.sections()):
                section_name = config[section]['name']
                print(f'({section}) {section_name}')
            task['id'] = str(input())
        section = config[task['id']]
        name = section['name']
        print(f'Logging for task: {name}')
        config[task['id']][f'log_{self.time}'] = task['message']
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def summarise_the_day(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        for section in config.sections():

            print(config[section]['name'], ':', config[section]['description'])
            usefulness = input('How useful was this task to your day? (1 (I feel accomplished), 5 (I barely remember this) \n')
            completed = input('Did you complete this task? (N/y) \n')
            notes = input('Notes for the completion or incompletion of this task')

            config[section]['usefulness'] = usefulness
            config[section]['completed'] = completed
            config[section]['completed_notes'] = notes

        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

        print('You logged the most messages for...')
        print('You complete {}/{} tasks')
        print('Thank you for logging your day! Have a good night!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log tasks for the day')
    parser.add_argument('-a', choices=['log', 'task', 'summarise'], help='add new task')
    parser.add_argument('-t', type=str, help='Provide task name or id')
    parser.add_argument('-td', type=str, help='Provide task description')
    parser.add_argument('-te', type=str, help='Provide task estimate')
    parser.add_argument('-l', type=str, help='Add log for task')


    args = parser.parse_args()

    timelog = TimeLog()
    if args.a == 'task':
        task = {'name': args.t, 'desc': args.td, 'est_time': args.te}
        timelog.create_task(task)

    if args.a == 'log':
        task = {'id': args.t, 'message': args.l}
        timelog.add_log(task)

    if args.a == 'summarise':
        timelog.summarise_the_day()



