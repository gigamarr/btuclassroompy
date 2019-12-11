from classroom import Classroom

class Menu:

    def __init__(self, classroom):
        self.interface = '''
\n
___________________________________________________________________________________________________

[1] Check Balance | [2] List Messages | [3] Read Message | [4] List Courses | [5] List Course Points

____________________________________________________________________________________________________
\n
'''
        self.actions = {
                '1':classroom.get_balance,
                '2':classroom.list_messages,
                '3':classroom.read_message,
                '4':classroom.list_courses,
                '5':classroom.list_course_points
        }

def main():
    username = input("Enter classroom username: ")
    password = input("Enter classroom password: ")
    classroom = Classroom(username, password)
    menu = Menu(classroom)
    print(menu.interface)
    while True:
        try:
            action = input("Enter number for action: ")
            print("\n")
            if action == '3':
                message_id = input("Enter ID of the message: ")
                print("\n")
                print(menu.actions[action](message_id))
            elif action == '5':
                course_id = input("Enter a course ID: ")
                print(menu.actions[action](course_id, classroom))
            else:
                print(menu.actions[action]())
            print(menu.interface)
        except KeyError:
            print("Action doesn't exist")
        except IndexError:
            print("Out of index.")

if __name__ == "__main__":
    main()
