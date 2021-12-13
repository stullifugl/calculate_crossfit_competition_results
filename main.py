import python_files.setup_workouts as setup_workouts
import python_files.calculate_results as calculate_results
import python_files.consts as consts

def main():
    # print("1: Setup workouts based on settings")
    # print("2: Calculate workout results based on inputs")
    # val = input("Choose what you wish to do: ")

    # if val == '1':
    #     if consts.SETUPWORKOUTS == False:
    #         print("Setting up workouts is disabled in consts, change and run again")
    #     else:
    #         if consts.ADDRANDOMSCORES:
    #             print("Random scores will be added to the workouts")
    #         setup_workouts.setupWorkouts()

    # if val == '2':
    #     calculate_results.calculateWorkouts()

    # setup_workouts.setupTeams()

    # setup_workouts.setupWorkouts()
    calculate_results.calculateWorkouts()

main()
